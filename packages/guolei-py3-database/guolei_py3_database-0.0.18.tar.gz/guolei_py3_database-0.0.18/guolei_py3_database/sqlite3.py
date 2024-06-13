#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
sqlite3 Class Library
-------------------------------------------------
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_database
=================================================
"""

import sqlite3
from typing import Union

from addict import Dict

CURSOR_FUNC_FETCHONE = "CURSOR_FUNC_FETCHONE"
CURSOR_FUNC_FETCHALL = "CURSOR_FUNC_FETCHALL"
CURSOR_PROP_LASTROWID = "CURSOR_PROP_LASTROWID"
CURSOR_PROP_ROWCOUNT = "CURSOR_PROP_ROWCOUNT"
CURSOR_PROP_DESCRIPTION = "CURSOR_PROP_DESCRIPTION"


class Database(object):
    """
    Database Class
    """

    def __init__(
            self,
            connect_args: Union[tuple, list] = (),
            connect_kwargs: Union[dict, Dict] = Dict({}),
    ):
        """
        Database construct function
        :param connect_args: sqlite3.connect args
        :param connect_kwargs: sqlite3.connect kwargs
        """
        self._connect_args = connect_args
        self._connect_kwargs = connect_kwargs
        self._connect: sqlite3.Connection = None

    @property
    def connect_args(self) -> Union[tuple, list]:
        """
        sqlite3.connect args
        :return:
        """
        return self._connect_args

    @connect_args.setter
    def connect_args(self, value: Union[tuple, list]):
        """
        sqlite3.connect args
        :param value:
        :return:
        """
        self._connect_args = value

    @property
    def connect_kwargs(self) -> Union[dict, Dict]:
        """
        sqlite3.connect kwargs
        :return:
        """
        return self._connect_kwargs

    @connect_kwargs.setter
    def connect_kwargs(self, value: Union[dict, Dict]):
        """
        sqlite3.connect kwargs
        :param value:
        :return:
        """
        self._connect_kwargs = value

    @property
    def connect(self) -> sqlite3.Connection:
        """
        sqlite3.Connection
        :return:
        """
        return self._connect

    def open_connect(self, row_factory=sqlite3.Row) -> bool:
        """
        open sqlite3 connect
        :param row_factory: row_factory
        :return:
        """
        self.connect_kwargs = Dict(self.connect_kwargs)
        self._connect = sqlite3.connect(*self.connect_args, **self.connect_kwargs.to_dict())
        self._connect.row_factory = row_factory
        return True

    def close_connect(self) -> bool:
        """
        close sqlite3 connect
        :return:
        """
        if isinstance(self.connect, sqlite3.Connection):
            self.connect.close()
            return True
        return False

    def executescript(self, sql_script: str = "") -> int:
        """
        call cursor.executescript
        :param sql_script:
        :return:
        """
        if not isinstance(self.connect, sqlite3.Connection):
            raise ValueError(f"connect:{self.connect} must be sqlite3.Connection")
        if not isinstance(sql_script, str) or not len(sql_script):
            raise ValueError(f"sql:{sql_script} must be string and not empty")
        try:
            cursor = self.connect.cursor()
            cursor.executescript(sql_script)
            self.connect.commit()
            return cursor.rowcount
        except Exception as error:
            self.connect.rollback()
            raise error
        finally:
            if isinstance(cursor, sqlite3.Cursor):
                cursor.close()

    def executemany(self, sql: str = "", seq_of_parameters=()) -> int:
        """
        call cursor.executemany
        :param sql:
        :param seq_of_parameters:
        :return:
        """
        if not isinstance(self.connect, sqlite3.Connection):
            raise ValueError(f"connect:{self.connect} must be sqlite3.Connection")
        if not isinstance(sql, str) or not len(sql):
            raise ValueError(f"sql:{sql} must be string and not empty")
        if not seq_of_parameters:
            seq_of_parameters = ()
        try:
            cursor = self.connect.cursor()
            cursor.executemany(sql, seq_of_parameters)
            self._connect.commit()
            return cursor.rowcount
        except Exception as error:
            self._connect.rollback()
            raise error
        finally:
            if isinstance(cursor, sqlite3.Cursor):
                cursor.close()

    def execute(self, sql: str = "", parameters=(), cursor_func_or_prop=CURSOR_PROP_ROWCOUNT):
        """
        call cursor.execute
        :param sql: sql
        :param parameters: parameters
        :param cursor_func_or_prop: return cursor func or prop
        :return:
        """
        if not isinstance(self.connect, sqlite3.Connection):
            raise ValueError(f"connect:{self.connect} must be sqlite3.Connection")
        if not isinstance(sql, str) or not len(sql):
            raise ValueError(f"sql:{sql} must be string and not empty")
        if not parameters:
            parameters = ()
        try:
            cursor = self.connect.cursor()
            cursor.execute(sql, parameters)
            self.connect.commit()
            if isinstance(cursor_func_or_prop, str) and len(cursor_func_or_prop):
                if cursor_func_or_prop == CURSOR_FUNC_FETCHONE:
                    return Dict(dict(cursor.fetchone()))
                if cursor_func_or_prop == CURSOR_FUNC_FETCHALL:
                    return [Dict(dict(i)) for i in list(cursor.fetchall())]
                if cursor_func_or_prop == CURSOR_PROP_LASTROWID:
                    return cursor.lastrowid
                if cursor_func_or_prop == CURSOR_PROP_ROWCOUNT:
                    return cursor.rowcount
                if cursor_func_or_prop == CURSOR_PROP_DESCRIPTION:
                    return cursor.description
            return cursor.rowcount
        except Exception as error:
            self.connect.rollback()
            raise error
        finally:
            if isinstance(cursor, sqlite3.Cursor):
                cursor.close()

    def rowcount(self, sql: str = "", parameters=()):
        """
        call cursor.execute and return cursor.rowcount
        :param sql:
        :param parameters:
        :return:
        """
        return self.execute(sql=sql, parameters=parameters, cursor_func_or_prop=CURSOR_PROP_ROWCOUNT)

    def lastrowid(self, sql: str = "", parameters=None):
        """
        call cursor.execute and return cursor.lastrowid
        :param sql:
        :param parameters:
        :return:
        """
        return self.execute(sql=sql, parameters=parameters, cursor_func_or_prop=CURSOR_PROP_LASTROWID)

    def description(self, sql: str = "", parameters=None):
        """
        call cursor.execute and return cursor.description
        :param sql:
        :param parameters:
        :return:
        """
        return self.execute(sql=sql, parameters=parameters, cursor_func_or_prop=CURSOR_PROP_DESCRIPTION)

    def fetchone(self, sql: str = "", parameters=None):
        """
        call cursor.execute and return cursor.fetchone
        :param sql:
        :param parameters:
        :return:
        """
        return self.execute(sql=sql, parameters=parameters, cursor_func_or_prop=CURSOR_FUNC_FETCHONE)

    def fetchall(self, sql: str = "", parameters=None):
        """
        call cursor.execute and return cursor.fetchall
        :param sql:
        :param parameters:
        :return:
        """
        return self.execute(sql=sql, parameters=parameters, cursor_func_or_prop=CURSOR_FUNC_FETCHALL)
