"""
Examples
--------
>>> import sqlexecutorx as db
>>> db.init('db.sqlite3', driver='sqlite3', show_sql=True, debug=True)
Engine.SQLITE
>>> sql = 'insert into person(name, age) values(%s, %s)'
>>> db.execute(sql, '张三', 20)
1
>>> sql = 'SELECT id, name, age FROM person WHERE name=%s and age=%s'
>>> db.select(sql, '张三', 20)
[(3, '张三', 20)]
>>> db.select_one(sql, '张三', 20)
(3, '张三', 20)
>>> db.query(sql, '张三', 20)
[{'id': 3, 'name': '张三', 'age': 20}]
>>> db.query_one(sql, '张三', 20)
{'id': 3, 'name': '张三', 'age': 20}
>>> sql = 'SELECT count(1) FROM person WHERE name=%s and age=%s LIMIT 1'
>>> db.get(sql, '张三', 20)
1
"""

from .core import (
    init,
    connection,
    transaction,
    with_connection,
    with_transaction,
    get_connection,
    close,
    execute,
    save,
    get,
    select,
    select_one,
    query,
    query_one,
    do_select,
    do_select_one,
    batch_execute
)
from .engine import Engine, Driver
from .support import DBError, Dict


__all__ = [
    'init',
    'connection',
    'transaction',
    'with_connection',
    'with_transaction',
    'get_connection',
    'close',
    'execute',
    'save',
    'get',
    'select',
    'select_one',
    'query',
    'query_one',
    'do_select',
    'do_select_one',
    'batch_execute',
    'DBError',
    'Dict',
    'Engine',
    'Driver'
]
