# !/usr/bin/env python3
# -*- coding:utf-8 -*-

import functools
from typing import List, Tuple
from .log_support import logger
from .engine import Engine, Driver
from .init_import import import_driver
from .sql_support import limit_one_sql
from .log_support import do_sql_log, do_save_log, batch_sql_log
from .constant import PARAM_DRIVER, PARAM_DEBUG, PARAM_POOL_SIZE, MODULE, PARAM_SHOW_SQL
from .support import DBCtx, ConnectionCtx, TransactionCtx, try_commit, DB_LOCK, Dict, MultiColumnsError, is_tuple_or_list

_DB_CTX = None
_POOLED = False
_SHOW_SQL = False


def init(*args, **kwargs) -> Engine:
    """
    Compliant with the Python DB API 2.0 (PEP-249).

    Addition parameters:
    :param driver=None: str|Driver, import driver, 'import pymysql'
    :param pool_size=0: int, default 0, size of connection pool
    :param show_sql=False: bool,  if True, print sql
    :param debug=False: bool, if True, print debug context

    Other parameters of connection pool refer to DBUtils: https://webwareforpython.github.io/DBUtils/main.html#pooleddb-pooled-db

    Examples
    --------
    >>> import sqlexecutorx as db
    >>> db.init('db.sqlite3', driver='sqlite3', show_sql=True debug=True)
    >>> or
    >>> db.init("postgres://user:password@127.0.0.1:5432/testdb", driver='psycopg2', pool_size=5, debug=True)
    >>> or
    >>> db.init(user='root', password='xxx', host='127.0.0.1', port=3306, database='testdb', driver='pymysql')
    """

    global _DB_CTX
    global _SHOW_SQL
    
    if _DB_CTX is not None:
        logger.warn('Database is already initialized.')
        return None
    
    pool_size = 0
    _SHOW_SQL = kwargs.pop(PARAM_SHOW_SQL) if PARAM_SHOW_SQL in kwargs else False
    driver = kwargs.pop(PARAM_DRIVER) if PARAM_DRIVER in kwargs else None
    engine, driver_name, creator = import_driver(driver, *args, **kwargs)
    prepared = Driver.MYSQL_CONNECTOR.value == driver_name
    if PARAM_DEBUG in kwargs and kwargs.pop(PARAM_DEBUG):
        from logging import DEBUG
        logger.setLevel(DEBUG)

    if PARAM_POOL_SIZE in kwargs:
        # mysql.connector 用自带连接池
        pool_size = kwargs[PARAM_POOL_SIZE] if prepared else kwargs.pop(PARAM_POOL_SIZE)

    pool_args = ['mincached', 'maxcached', 'maxshared', 'maxconnections', 'blocking', 'maxusage', 'setsession', 'reset', 'failures', 'ping']
    pool_kwargs = {key: kwargs.pop(key) for key in pool_args if key in kwargs}
    connect = lambda: creator.connect(*args, **kwargs)
    if pool_size >= 1 and not prepared:
        from .pooling import pooled_connect
        global _POOLED
        _POOLED = True
        connect = pooled_connect(connect, pool_size, **pool_kwargs)

    with DB_LOCK:
        if _DB_CTX is None:
            _DB_CTX = DBCtx(connect=connect, prepared=prepared)
            if pool_size > 0:
                logger.info(
                    "Inited database <%s> of %s with driver: '%s' and pool size: %d." % (hex(id(_DB_CTX)), engine.value,
                                                                                         driver_name, pool_size))
            else:
                logger.info(
                    "Inited database <%s> of %s with driver: '%s'." % (hex(id(_DB_CTX)), engine.value, driver_name))
        else:
            logger.warn('Database is already initialized.')

    return engine


def connection():
    """
    Return ConnectionCtx object that can be used by 'with' statement:

    Examples
    --------
    >>> from sqlexecutorx import connection
    >>> with connection():
    >>>     pass
    """

    global _DB_CTX
    return ConnectionCtx(_DB_CTX)


def with_connection(func):
    """
    Decorator for reuse connection.

    Examples
    --------
    >>> from sqlexecutorx import with_connection
    >>> @with_connection
    >>> def foo(*args, **kw):
    >>>     f1()
    >>>     f2()
    """

    global _DB_CTX

    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with ConnectionCtx(_DB_CTX):
            return func(*args, **kw)
    return _wrapper


def transaction():
    """
    Create a transaction object so can use with statement:

    Examples
    --------
    >>> from sqlexecutorx import with_connection
    >>> with transaction():
    >>>     pass
    >>> with transaction():
    >>>      insert(...)
    >>>      update(... )
    """

    global _DB_CTX
    return TransactionCtx(_DB_CTX)


def with_transaction(func):
    """
    A decorator that makes function around transaction.

    Examples
    --------
    >>> from sqlexecutorx import with_connection
    >>> @with_transaction
    >>> def update_profile(id, name, rollback):
    >>>      u = dict(id=id, name=name, email='%s@test.org' % name, passwd=name, last_modified=time.time())
    >>>      insert('person', **u)
    >>>      r = update('update person set passwd=%s where id=%s', name.upper(), id)
    """
    global _DB_CTX

    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with TransactionCtx(_DB_CTX):
            return func(*args, **kw)
    return _wrapper


def get_connection():
    global _DB_CTX
    _DB_CTX.try_init()
    return _DB_CTX.connection


def close():
    global _DB_CTX
    global _POOLED

    if _POOLED:
        from .pooling import close_pool
        close_pool()
        _POOLED = False

    if _DB_CTX is not None:
        _DB_CTX.release()
        _DB_CTX = None


@with_connection
def execute(sql: str, *args) -> int:
    """
    Execute sql return effect rowcount

    :param sql: SQL
    :param args:
    :return: Effect rowcount

    Examples
    --------
    >>> import sqlexecutorx as db
    >>> sql = 'INSERT INTO person(name, age) VALUES(%s, %s)'
    >>> db.execute(sql, '张三', 20)
    1
    """

    global _DB_CTX
    global _SHOW_SQL
    cursor = None
    if _SHOW_SQL:
        do_sql_log(MODULE, 'execute', sql, *args)
    try:
        cursor = _DB_CTX.connection.cursor()
        cursor.execute(sql, args)
        result = cursor.rowcount
        try_commit(_DB_CTX)
        return result
    finally:
        if cursor:
            cursor.close()


@with_connection
def save(select_key: str, sql: str, *args):
    """
    Execute sql return primary key

    :param select_key:
    :param sql: SQL
    :param args:
    :return: Primary key

    Examples
    --------
    >>> import sqlexecutorx as db
    >>> sql = 'INSERT INTO person(name, age) VALUES(%s, %s)'
    >>> db.save('SELECT LAST_INSERT_ID()', sql, '张三', 20)
    3
    """

    global _DB_CTX
    global _SHOW_SQL
    cursor = None
    if _SHOW_SQL:
        do_save_log(MODULE, 'save', select_key, sql, *args)
    try:
        cursor = _DB_CTX.connection.cursor()
        cursor.execute(sql, args)
        cursor.execute(select_key)
        result = cursor.fetchone()[0]
        try_commit(_DB_CTX)
        return result
    finally:
        if cursor:
            cursor.close()


def get(sql: str, *args):
    """
    Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
    MultiColumnsError: Expect only one column.

    Examples
    --------
    >>> import sqlexecutorx as db
    >>> sql = 'SELECT count(1) FROM person WHERE name=%s and age=%s LIMIT 1'
    >>> db.get(sql, '张三', 20)
    1
    """

    result = select_one(sql, *args)
    if result:
        if len(result) == 1:
            return result[0]
        msg = "Exec func 'sqlexecutorx.%s' expect only one column but %d." % ('do_get', len(result))
        logger.error('%s  \n\t sql: %s \n\t args: %s' % (msg, sql, args))
        raise MultiColumnsError(msg)
    return None


def select(sql: str, *args) -> List[Tuple]:
    """
    Examples
    --------
    >>> import sqlexecutorx as db
    >>> sql = 'SELECT id, name, age FROM person WHERE name=%s and age=%s'
    >>> db.select(sql, '张三', 20)
    [(3, '张三', 20)]
    """
    return do_select(sql, *args)[0]


def select_one(sql: str, *args) -> Tuple:
    """
    Examples
    --------
    >>> import sqlexecutorx as db
    >>> sql = 'SELECT id, name, age FROM person WHERE name=%s and age=%s LIMIT 1'
    >>> db.select_one(sql, '张三', 20)
    (3, '张三', 20)
    """
    return do_select_one(sql, *args)[0]


def query(sql: str, *args) -> List[dict]:
    """
    Execute select SQL and return list results(dict).

    Examples
    --------
    >>> import sqlexecutorx as db
    >>> sql = 'SELECT id, name, age FROM person WHERE name=%s and age=%s'
    >>> db.query(sql, '张三', 20)
    [{'id': 3, 'name': '张三', 'age': 20}]
    """
    results, description = do_select(sql, *args)
    if results and description:
        names = list(map(lambda x: x[0], description))
        return list(map(lambda x: Dict(names, x), results))
    return results


def query_one(sql: str, *args) -> dict:
    """
    Execute select SQL and return unique result(dict), SQL contain 'limit'.

    Examples
    --------
    >>> import sqlexecutorx as db
    >>> sql = 'SELECT id, name, age FROM person WHERE name=%s and age=%s LIMIT 1'
    >>> db.query_one(sql, '张三', 20)
    {'id': 3, 'name': '张三', 'age': 20}
    """

    result, description = do_select_one(sql, *args)
    if result and description:
        names = list(map(lambda x: x[0], description))
        return Dict(names, result)
    return result


@with_connection
def do_select(sql: str, *args) -> Tuple[List, Tuple]:
    """
    Execute select SQL and return results and description

    Examples
    --------
    >>> import sqlexecutorx as db
    >>> sql = 'SELECT id, name, age FROM person WHERE name=%s and age=%s limit 1'
    >>> db.do_select(sql, '张三', 20)
    ([(3, '张三', 20)], (('id', None, None), ('name', None, None), ('age', None, None)))
    """

    global _DB_CTX
    global _SHOW_SQL
    cursor = None

    if _SHOW_SQL:
        do_sql_log(MODULE, 'do_select', sql, *args)

    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        return cursor.fetchall(), cursor.description
    finally:
        if cursor:
            cursor.close()


@with_connection
def do_select_one(sql: str, *args) -> Tuple[Tuple, Tuple]:
    """
    Execute select SQL and return result and description

    Examples
    --------
    >>> import sqlexecutorx as db
    >>> sql = 'SELECT id, name, age FROM person WHERE name=%s and age=%s limit 1'
    >>> db.do_select_one(sql, '张三', 20)
    ((3, '张三', 20), (('id', None, None), ('name', None, None), ('age', None, None)))
    """

    global _DB_CTX
    global _SHOW_SQL
    cursor = None

    sql = limit_one_sql(sql)

    if _SHOW_SQL:
        do_sql_log(MODULE, 'do_select_one', sql, *args)

    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        return cursor.fetchone(), cursor.description
    finally:
        if cursor:
            cursor.close()


@with_connection
def batch_execute(sql: str, *args) -> int:
    """
    Batch execute sql return effected rowcount

    :param sql: SQL to execute
    :param args: All number must have same size.
    :return: Effect rowcount

    Examples
    --------
    >>> import sqlexecutorx as db
    >>> args = [('张三', 20), ('李四', 28)]
    >>> sql = 'INSERT INTO person(name, age) VALUES(%s, %s)'
    >>> db.batch_execute(sql, args)
    2
    >>> db.batch_execute(sql, *args)
    2
    """

    global _DB_CTX
    global _SHOW_SQL
    cursor = None
    assert args, "*args must not be empty."
    assert is_tuple_or_list(args[0]), "args must not be Tuple or List."
    
    if len(args) == 1 and len(args[0]) > 0 and is_tuple_or_list(args[0][0]):
        args = args[0]
        
    if _SHOW_SQL:
        batch_sql_log(MODULE, 'batch_execute', sql, args)

    try:
        cursor = _DB_CTX.cursor()
        cursor.executemany(sql, args)
        effect_rowcount = cursor.rowcount
        try_commit(_DB_CTX)
        return effect_rowcount
    finally:
        if cursor:
            cursor.close()
