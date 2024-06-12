# !/usr/bin/env python3
# -*- coding:utf-8 -*-

from typing import Sequence, Tuple, List, Union
from sqlexecutorx import batch_execute as _batch_execute
from sqlexecutorx.support import is_tuple_or_list
from .loader import Loader
from . import exec, sql_support
from .dialect import Dialect, Engine
from .constant import LIMIT_1, SELECT_COUNT
from .sql_support import get_table_select_sql


class TablePageExec:

    def __init__(self, table_exec, page_num, page_size):
        self.table_exec = table_exec
        self.page_num = page_num
        self.page_size = page_size

    def select(self, *columns) -> List[Tuple]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').page(1, 10).select('id', 'name', 'age')
        [(3, '张三', 20)]
        """
        sql = get_table_select_sql(self.table_exec.table, '', 0, *columns)
        return self.table_exec.exec.do_select_page(sql, self.page_num, self.page_size)

    def query(self, *columns) -> List[dict]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').page(1, 10).query('id', 'name', 'age')
        [{'id': 3, 'name': '张三', 'age': 20}]
        """
        sql = get_table_select_sql(self.table_exec.table, '', 0, *columns)
        return self.table_exec.exec.do_query_page(sql, self.page_num, self.page_size)


class ColumnPageExec:

    def __init__(self, table_page_exec: TablePageExec, *columns):
        self.table_page_exec = table_page_exec
        self.columns = columns

    def select(self) -> List[Tuple]:
        """
        Select data from table and return list results(tuple).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').page(1, 10).select()
        [(3, '张三', 20)]
        """
        return self.table_page_exec.select(*self.columns)

    def query(self) -> List[dict]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').page(1, 10).query()
        [{'id': 3, 'name': '张三', 'age': 20}]
        """
        return self.table_page_exec.query(*self.columns)


class WherePageExec:

    def __init__(self, where_exec, page_num, page_size):
        self.where_exec = where_exec
        self.page_num = page_num
        self.page_size = page_size

    def select(self, *columns) -> List[Tuple]:
        """
        Select data from table and return list results(tuple).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三', age=20).page(1, 10).select('id', 'name', 'age')
        [(3, '张三', 20)]
        """
        sql, args = self.where_exec.get_select_sql_args(*columns)
        return self.where_exec.exec.do_select_page(sql, self.page_num, self.page_size, *args)

    def query(self, *columns) -> List[dict]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三', age=20).page(1, 10).query('id', 'name', 'age')
        [{'id': 3, 'name': '张三', 'age': 20}]
        """
        sql, args = self.where_exec.get_select_sql_args(*columns)
        return self.where_exec.exec.do_query_page(sql, self.page_num, self.page_size, *args)


class ColumnWherePageExec:

    def __init__(self, where_page_exec: WherePageExec, *columns):
        self.where_page_exec = where_page_exec
        self.columns = columns

    def select(self) -> List[Tuple]:
        """
        Select data from table and return list results(tuple).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20).page(1, 10).select()
        [(3, '张三', 20)]
        """
        return self.where_page_exec.select(*self.columns)

    def query(self) -> List[dict]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20).page(1, 10).query()
        [{'id': 3, 'name': '张三', 'age': 20}]
        """
        return self.where_page_exec.query(*self.columns)


class ColumnWhereExec:

    def __init__(self, where_exec, *columns):
        self._where_exec = where_exec
        self.columns = columns

    def get(self):
        """
        Select data from table and expected one int and only one int result, SQL contain 'limit'.
        MultiColumnsError: Expect only one column.

        sqlexecx.table('person').columns('name').where(id=1).get()
        """
        return self._where_exec.get(self.columns[0])

    def select(self) -> List[Tuple]:
        """
        Select data from table and return list results(tuple).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20).select()
        [(3, '张三', 20)]
        """
        return self._where_exec.select(*self.columns)

    def select_one(self) -> Tuple:
        """
        Select data from table and return unique result(tuple), SQL contain 'limit'.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20).select_one()
        (3, '张三', 20)
        """
        return self._where_exec.select_one(*self.columns)

    def query(self) -> List[dict]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20).query()
        [{'id': 3, 'name': '张三', 'age': 20}]
        """
        return self._where_exec.query(*self.columns)

    def query_one(self) -> dict:
        """
        Select from table and return unique result(dict), SQL contain 'limit'.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20).query_one()
        {'id': 3, 'name': '张三', 'age': 20}
        """
        return self._where_exec.query_one(*self.columns)

    def to_df(self):
        """
        Select from table and return pandas DataFrame instance.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db..table('person').columns('id', 'name', 'age').where(name__eq='李四').to_df()
        """
        return self._where_exec.load(*self.columns).to_df()

    def to_csv(self, file_name: str, delimiter=',', header=True, encoding='utf-8'):
        """
        Select from table and sava as a csv file.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db..table('person').columns('id', 'name', 'age').where(name__eq='李四').to_csv('test.csv')
        """
        self._where_exec.load(*self.columns).to_csv(file_name, delimiter, header, encoding)

    def to_json(self, file_name: str, encoding='utf-8'):
        """
        Select from table and sava as a json file.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db..table('person').columns('id', 'name', 'age').where(name__eq='李四').to_json('test.json')
        """
        self._where_exec.load(*self.columns).to_json(file_name, encoding)

    def page(self, page_num=1, page_size=10) -> ColumnWherePageExec:
        """
        Get a ColumnWherePageExec instance

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20).page(1, 10)
        ColumnWherePageExec()
        """
        return ColumnWherePageExec(WherePageExec(self._where_exec, page_num, page_size), *self.columns)


class WhereExec:

    def __init__(self, _exec, table_name, **kwargs):
        self.exec = _exec
        self.table = table_name
        self.where_condition = kwargs

    def get(self, column: str):
        """
        Select data from table and expected one int and only one int result, SQL contain 'limit'.

        MultiColumnsError: Expect only one column.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(id=3).get('name')
        张三
        """
        sql, args = self.get_select_one_sql_args(column)
        return self.exec.do_get(sql, *args, LIMIT_1)

    def count(self) -> int:
        """
        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三').count()
        1
        """
        return self.get(SELECT_COUNT)

    def exists(self) -> bool:
        """
        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三').exists()
        True
        """
        return self.get(1) == 1

    def select(self, *columns) -> List[Tuple]:
        """
        Select data from table and return list results(tuple).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三', age=20).select('id', 'name', 'age')
        [(3, '张三', 20)]
        """
        sql, args = self.get_select_sql_args(*columns)
        return self.exec.do_select(sql, *args)

    def select_one(self, *columns) -> Tuple:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三', age=20).select_one('id', 'name', 'age')
        (3, '张三', 20)
        """
        sql, args = self.get_select_one_sql_args(*columns)
        return self.exec.do_select_one(sql, *args, LIMIT_1)

    def query(self, *columns) -> List[dict]:
        """
        Select data from table and return list results(tuple).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三', age=20).query('id', 'name', 'age')
        [{'id': 3, 'name': '张三', 'age': 20}]
        """
        sql, args = self.get_select_sql_args(*columns)
        return self.exec.do_query(sql, *args)

    def query_one(self, *columns) -> dict:
        """
        Select from table and return unique result(dict), SQL contain 'limit'.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三', age=20).query_one('id', 'name', 'age')
        {'id': 3, 'name': '张三', 'age': 20}
        """
        sql, args = self.get_select_one_sql_args(*columns)
        return self.exec.do_query_one(sql, *args, LIMIT_1)

    def delete(self) -> int:
        """
        Delete and return effect rowcount.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三').delete()
        1
        """
        where, args, _ = get_where_arg_limit(**self.where_condition)
        sql = 'DELETE FROM %s %s' % (Dialect.get_dialect_str(self.table), where)
        if Dialect.curr_engine() in (Engine.MYSQL, Engine.SQLITE):
            sql = '{} LIMIT ?'.format(sql)
            args = [*args, LIMIT_1]
        return self.exec.do_execute(sql, *args)

    def update(self, **kwargs) -> int:
        """
        Update and return effect rowcount.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三').update(name='李四', age=45)
        1
        """
        where, args, _ = get_where_arg_limit(**self.where_condition)
        update_cols, update_args = zip(*kwargs.items())
        args = [*update_args, *args]
        update_cols = ', '.join(['{} = ?'.format(Dialect.get_dialect_str(col)) for col in update_cols])
        sql = 'UPDATE {} SET {} {}'.format(Dialect.get_dialect_str(self.table), update_cols, where)
        if Dialect.curr_engine() in (Engine.MYSQL, Engine.SQLITE):
            sql = '{} LIMIT ?'.format(sql)
            args = [*args, LIMIT_1]
        return self.exec.do_execute(sql, *args)

    def load(self, *columns) -> Loader:
        """
        Get a Loader instance

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三', age=20).load('id', 'name', 'age')
        Loader()
        """
        sql, args = self.get_select_sql_args(*columns)
        return self.exec.do_load(sql, *args)

    def columns(self, *columns) -> ColumnWhereExec:
        """
        Get a ColumnWhereExec instance

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三', age=20).columns('id', 'name', 'age')
        ColumnWhereExec()
        """
        return ColumnWhereExec(self, *columns)

    def page(self, page_num=1, page_size=10) -> WherePageExec:
        """
        Get a WherePageExec instance

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三', age=20).page(1, 10)
        WherePageExec()
        """
        return WherePageExec(self, page_num, page_size)

    def get_select_sql_args(self, *columns):
        where, args, limit = get_where_arg_limit(**self.where_condition)
        sql = get_table_select_sql(self.table, where, limit, *columns)
        if limit:
            if isinstance(limit, int):
                args = [*args, limit]
            else:
                args = [*args, *limit]
        return sql, args

    def get_select_one_sql_args(self, *columns):
        where, args, _ = get_where_arg_limit(**self.where_condition)
        sql = get_table_select_sql(self.table, where, LIMIT_1, *columns)
        return sql, args


class LimitExec:

    def __init__(self, _exec, table_name: str, limit: Union[int, Tuple[int], List[int]]):
        self.exec = _exec
        self.table = table_name
        self.limit = limit

    def select(self, *columns) -> List[Tuple]:
        """
        Select data from table and return list results(tuple).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').limit(10).select('id', 'name', 'age')
        [(3, '张三', 20)]
        """
        sql = get_table_select_sql(self.table, '', self.limit, *columns)
        return self.exec.do_select(sql, self.limit)

    def query(self, *columns) -> List[Tuple]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').limit(10).query('id', 'name', 'age')
        [{'id': 3, 'name': '张三', 'age': 20}]
        """
        sql = get_table_select_sql(self.table, '', self.limit, *columns)
        if isinstance(self.limit, int):
            return self.exec.do_query(sql, self.limit)
        else:
            return self.exec.do_query(sql, *self.limit)


class ColumnLimitExec:

    def __init__(self, limit_exec: LimitExec, *columns):
        self.limit_exec = limit_exec
        self.columns = columns

    def select(self) -> List[Tuple]:
        """
        Select data from table and return list results(tuple).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').limit(10).select()
        [(3, '张三', 20)]
        """
        return self.limit_exec.select(*self.columns)

    def query(self) -> List[Tuple]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').limit(10).query()
        [{'id': 3, 'name': '张三', 'age': 20}]
        """
        return self.limit_exec.query(*self.columns)


class ColumnExec:

    def __init__(self, table_exec, *columns):
        self.table_exec = table_exec
        self.columns = columns

    def insert(self, *args) -> int:
        """
        Insert data into table, return effect rowcount.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('name', 'age').insert('张三', 20)
        1
        """
        assert args, 'args expected but empty.'
        sql = sql_support.insert_sql(self.table_exec.table.strip(), self.columns)
        return self.table_exec.exec.execute(sql, *args)

    def batch_insert(self, *args) -> int:
        """
        Batch insert data into table and return effect rowcount

        Examples
        --------
        >>> import sqlexecx as db
        >>> args = [('张三', 20), ('李四', 28)]
        >>> db.table('person').columns('name', 'age').batch_insert(args)
        2
        >>> db.table('person').columns('name', 'age').batch_insert(*args)
        2
        """
        sql = sql_support.insert_sql(self.table_exec.table.strip(), self.columns)
        if len(args) == 1 and is_tuple_or_list(args[0]) and len(args[0]) > 0 and is_tuple_or_list(args[0][0]):
            args = args[0]
        return _batch_execute(sql, *args)

    def get(self):
        """
        Select data from table and expected one int and only one int result, SQL contain 'limit'.

        MultiColumnsError: Expect only one column.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('count(1)').get()
        3
        """
        return self.table_exec.get(*self.columns)

    def select(self) -> List[Tuple]:
        """
        Select data from table and return list results(tuple).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').select()
        [(3, '张三', 20)]
        """
        return self.table_exec.select(*self.columns)

    def select_one(self) -> Tuple:
        """
        Select data from table and return unique result(tuple), SQL contain 'limit'.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').select_one()
        (3, '张三', 20)
        """
        return self.table_exec.select_one(*self.columns)

    def query(self) -> List[dict]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').query()
        [{'id': 3, 'name': '张三', 'age': 20}]
        """
        return self.table_exec.query(*self.columns)

    def query_one(self) -> dict:
        """
        Select from table and return unique result(dict), SQL contain 'limit'.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').query_one()
        {'id': 3, 'name': '张三', 'age': 20}
        """
        return self.table_exec.query_one(*self.columns)

    def to_df(self):
        """
        Select from table and return pandas DataFrame instance.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db..table('person').columns('id', 'name', 'age').to_df()
        """
        return self.table_exec.load(*self.columns).to_df()

    def to_csv(self, file_name: str, delimiter=',', header=True, encoding='utf-8'):
        """
        Select from table and sava as a csv file.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db..table('person').columns('id', 'name', 'age').to_csv('test.csv')
        """
        self.table_exec.load(*self.columns).to_csv(file_name, delimiter, header, encoding)

    def to_json(self, file_name: str, encoding='utf-8'):
        """
        Select from table and sava as a json file.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db..table('person').columns('id', 'name', 'age').to_json('test.json')
        """
        self.table_exec.load(*self.columns).to_json(file_name, encoding)

    def where(self, **kwargs) -> ColumnWhereExec:
        """
        Get a ColumnWhereExec instance

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').where(name='张三', age=20)
        ColumnWhereExec()
        """
        return ColumnWhereExec(self.table_exec.where(**kwargs), *self.columns)

    def page(self, page_num=1, page_size=10) -> ColumnPageExec:
        """
        Get a ColumnPageExec instance

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age').page(1, 10)
        ColumnPageExec()
        """
        return ColumnPageExec(TablePageExec(self.table_exec, page_num, page_size), *self.columns)

    def limit(self, limit: Union[int, Tuple[int], List[int]] = 10) -> ColumnLimitExec:
        """
        Get a ColumnLimitExec instance

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').limit(10)
        ColumnLimitExec()
        """
        return ColumnLimitExec(self.table_exec.limit(limit), *self.columns)


class TableExec:

    def __init__(self, _exec, table_name):
        self.exec = _exec
        self.table = table_name

    def insert(self, **kwargs) -> int:
        """
        Insert data into table, return effect rowcount.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').insert(name='张三', age=20)
        1
        """
        return self.exec.insert(self.table, **kwargs)

    def save(self, **kwargs):
        """
        Insert data into table, return primary key.

        :return: Primary key

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').save(name='张三', age=20)
        3
        """
        return self.exec.save(self.table, **kwargs)

    def save_select_key(self, select_key: str, **kwargs):
        """
        Insert data into table, return primary key.

        :param select_key: sql for select primary key
        :return: Primary key

        Examples
        --------
        >>> import sqlexecx as db
        >>> select_key = 'SELECT LAST_INSERT_ID()'
        >>> db.table('person').save_select_key(select_key, name='张三', age=20)
        3
        """
        return self.exec.save_select_key(select_key, self.table, **kwargs)

    def batch_insert(self, *args) -> int:
        """
        Batch insert data into table and return effect rowcount

        Examples
        --------
        >>> import sqlexecx as db
        >>> args = [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
        >>> db.table('person').batch_insert(*args)
        2
        """
        return self.exec.batch_insert(self.table, *args)

    def get(self, column: str):
        """
        Select data from table and expected one int and only one int result, SQL contain 'limit'.

        MultiColumnsError: Expect only one column.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').get('count(1)')
        3
        """
        sql = get_table_select_sql(self.table, '', LIMIT_1, column)
        return self.exec.do_get(sql, LIMIT_1)

    def count(self) -> int:
        """
        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').count()
        3
        """
        return self.get(SELECT_COUNT)

    def select(self, *columns) -> List[Tuple]:
        """
        Select data from table and return list results(tuple).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').select('id', 'name', 'age')
        [(3, '张三', 20)]
        """
        sql = get_table_select_sql(self.table, '', 0, *columns)
        return self.exec.do_select(sql)

    def select_one(self, *columns) -> Tuple:
        """
        Select data from table and return unique result(tuple), SQL contain 'limit'.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').do_select_one('id', 'name', 'age')
        (3, '张三', 20)
        """
        sql = get_table_select_sql(self.table, '', LIMIT_1, *columns)
        return self.exec.do_select_one(sql, LIMIT_1)

    def query(self, *columns) -> List[dict]:
        """
        Select data from table and return list results(dict).

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').query('id', 'name', 'age')
        [{'id': 3, 'name': '张三', 'age': 20}]
        """
        sql = get_table_select_sql(self.table, '', 0, *columns)
        return self.exec.do_query(sql)

    def query_one(self, *columns) -> dict:
        """
        Select data from table and return unique result(dict), SQL contain 'limit'.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').query_one('id', 'name', 'age')
        {'id': 3, 'name': '张三', 'age': 20}
        """
        sql = get_table_select_sql(self.table, '', LIMIT_1, *columns)
        return self.exec.do_query_one(sql, LIMIT_1)

    def load(self, *columns) -> Loader:
        """
        Select from table and return a Loader instance

        :return: Loader

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').load('id', 'name', 'age')
        Lodder()
        """
        sql = get_table_select_sql(self.table, '', 0, *columns)
        return self.exec.do_load(sql)

    def insert_from_df(self, df, columns: Tuple[str] = None):
        """
        Insert data into table from pandas DataFrame and return effected rowcount.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').insert_from_df(df)
        20
        """
        return self.exec.insert_from_df(df, self.table, columns)

    def insert_from_csv(self, file_name: str, delimiter=',', header=True, columns: Tuple[str] = None, encoding='utf-8'):
        """
        Insert data into table from a csv file and return effected rowcount.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').insert_from_csv('test.csv')
        20
        """
        return self.exec.insert_from_csv(file_name, self.table, delimiter, header, columns, encoding=encoding)

    def insert_from_json(self, file_name: str, encoding='utf-8'):
        """
        Insert data into table from a json file and return effected rowcount.

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').insert_from_json('test.json')
        20
        """
        return self.exec.insert_from_json(file_name, self.table, encoding=encoding)

    def truncate(self) -> int:
        """
        Truncate table and return effected rowcount

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').truncate()
        1
        """
        return self.exec.truncate(self.table)

    def drop(self) -> int:
        """
        Drop table and return effected rowcount

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').drop()
        1
        """
        return self.exec.drop(self.table)

    def where(self, **kwargs) -> WhereExec:
        """
        Get a WhereExec instance

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').where(name='张三', age=20)
        WhereExec()
        """
        return WhereExec(self.exec, self.table, **kwargs)

    def columns(self, *columns) -> ColumnExec:
        """
        Get a ColumnExec instance

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').columns('id', 'name', 'age')
        ColumnExec()
        """
        return ColumnExec(self, *columns)

    def page(self, page_num=1, page_size=10) -> TablePageExec:
        """
        Get a TablePageExec instance

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').page(1, 10)
        TablePageExec()
        """
        return TablePageExec(self,  page_num, page_size)

    def limit(self, limit: Union[int, Tuple[int], List[int]] = 10) -> LimitExec:
        """
        Get a LimitExec instance

        Examples
        --------
        >>> import sqlexecx as db
        >>> db.table('person').limit(10)
        LimitExec()
        """
        return LimitExec(self.exec, self.table, limit)


def table(table_name: str) -> TableExec:
    """
    Get a TableExec instance

    Examples
    --------
    >>> import sqlexecx as db
    >>> db.table('person')
    """
    table_name = table_name.strip()
    assert table_name, "Parameter 'table' must not be none"
    return TableExec(exec, table_name)


def get_condition_arg(k: str, v: object):
    if k.endswith("__eq"):
        return "{} = ?".format(Dialect.get_dialect_str(k[:-4])), v
    if k.endswith("__ne"):
        return "{} != ?".format(Dialect.get_dialect_str(k[:-4])), v
    if k.endswith("__gt"):
        return "{} > ?".format(Dialect.get_dialect_str(k[:-4])), v
    if k.endswith("__lt"):
        return "{} < ?".format(Dialect.get_dialect_str(k[:-4])), v
    if k.endswith("__ge"):
        return "{} >= ?".format(Dialect.get_dialect_str(k[:-4])), v
    if k.endswith("__gte"):
        return "{} >= ?".format(Dialect.get_dialect_str(k[:-5])), v
    if k.endswith("__le"):
        return "{} <= ?".format(Dialect.get_dialect_str(k[:-4])), v
    if k.endswith("__lte"):
        return "{} <= ?".format(Dialect.get_dialect_str(k[:-5])), v
    if k.endswith("__isnull"):
        return "{} is {}".format(Dialect.get_dialect_str(k[:-8]), 'null' if v else 'not null'), None
    if k.endswith("__in") and isinstance(v, Sequence) and not isinstance(v, str):
        return "{} in({})".format(Dialect.get_dialect_str(k[:-4]), ','.join(['?' for _ in v])), v
    if k.endswith("__in"):
        return "{} in({})".format(Dialect.get_dialect_str(k[:-4]), '?'), v
    if k.endswith("__not_in") and isinstance(v, Sequence) and not isinstance(v, str):
        return "{} not in({})".format(Dialect.get_dialect_str(k[:-8]), ','.join(['?' for _ in v])), v
    if k.endswith("__not_in"):
        return "{} not in({})".format(Dialect.get_dialect_str(k[:-8]), '?'), v
    if k.endswith("__like"):
        return "{} like ?".format(Dialect.get_dialect_str(k[:-6])), '%{}%'.format(v)
    if k.endswith("__startswith"):
        return "{} like ?".format(Dialect.get_dialect_str(k[:-12])), '{}%'.format(v)
    if k.endswith("__endswith"):
        return "{} like ?".format(Dialect.get_dialect_str(k[:-10])), '%{}'.format(v)
    if k.endswith("__contains"):
        return "{} like ?".format(Dialect.get_dialect_str(k[:-10])), '%{}%'.format(v)
    if k.endswith("__range") and isinstance(v, Sequence) and 2 == len(v) and not isinstance(v, str):
        col = k[:-7]
        return "{} >= ? and {} <= ?".format(Dialect.get_dialect_str(col), Dialect.get_dialect_str(col)), v
    if k.endswith("__between") and isinstance(v, Sequence) and 2 == len(v) and not isinstance(v, str):
        return "{} between ? and ?".format(Dialect.get_dialect_str(k[:-9])), v
    if k.endswith("__range") or k.endswith("__between"):
        return ValueError("Must is instance of Sequence with length 2 when use range or between statement")

    return "{} = ?".format(Dialect.get_dialect_str(k)), v


def get_where_arg_limit(**kwargs):
    where, args, limit = '', [], 0
    if 'limit' in kwargs:
        limit = kwargs.pop('limit')

    if kwargs:
        conditions, tmp_args = zip(*[get_condition_arg(k, v) for k, v in kwargs.items()])
        tmp_args = [arg for arg in tmp_args if arg is not None]

        for arg in tmp_args:
            if arg is not None:
                if isinstance(arg, Sequence) and not isinstance(arg, str):
                    args.extend(arg)
                else:
                    args.append(arg)
        where = 'WHERE {}'.format(' and '.join(conditions))

    return where, args, limit
