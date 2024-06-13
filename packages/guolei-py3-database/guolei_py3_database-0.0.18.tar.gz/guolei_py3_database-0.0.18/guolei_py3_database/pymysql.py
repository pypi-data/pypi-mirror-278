#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
pymysql Mysql Class Library
-------------------------------------------------
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_database
=================================================
"""
from typing import Union

import pymysql
from addict import Dict
from pymysql import Connect
from pymysql.cursors import DictCursor

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
        :param connect_args: pymysql.Connect args
        :param connect_kwargs:pymysql.Connect kwargs
        """
        self._connect_args = connect_args
        self._connect_kwargs = connect_kwargs
        self._connect: pymysql.Connect = None

    @property
    def connect_args(self) -> Union[tuple, list]:
        """
        pymysql.Connect args
        :return:
        """
        return self._connect_args

    @connect_args.setter
    def connect_args(self, value: Union[tuple, list]):
        """
        pymysql.Connect args
        :param value:
        :return:
        """
        self._connect_args = value

    @property
    def connect_kwargs(self) -> Union[dict, Dict]:
        """
        pymysql.Connect kwargs
        :return:
        """
        return self._connect_kwargs

    @connect_kwargs.setter
    def connect_kwargs(self, value: Union[dict, Dict]):
        """
        pymysql.Connect kwargs
        :param value:
        :return:
        """
        self._connect_kwargs = value

    @property
    def connect(self) -> pymysql.Connect:
        """
        pymysql.Connect
        :return:
        """
        return self._connect

    def open_connect(self) -> bool:
        """
        open pymysql.Connect
        :return:
        """
        self.connect_kwargs = Dict(self.connect_kwargs)
        self.connect_kwargs.setdefault("cursorclass", DictCursor)
        self._connect = pymysql.Connect(
            *self.connect_args,
            **self.connect_kwargs.to_dict()
        )
        return True

    def close_connect(self) -> bool:
        """
        close pymysql.Connect
        :return:
        """
        if isinstance(self.connect, Connect) and self.connect.open:
            self.connect.close()
            return True
        return False

    def transaction(self, queries: list = []) -> bool:
        """
        call cursor.execute in transaction
        :param queries:
        :return:
        """
        if not isinstance(self.connect, Connect) or not self.connect.open:
            raise ValueError("connect is Connect and connect must be open")
        if not isinstance(queries, list) or not len(queries):
            raise ValueError(f"queries:{queries} must be list and not empty")
        with self.connect.cursor() as cursor:
            try:
                self.connect.begin()
                for query in queries:
                    if isinstance(query, tuple):
                        cursor.execute(*query)
                    if isinstance(query, dict):
                        cursor.execute(**query)
                    if isinstance(query, str):
                        cursor.execute(query)
                self.connect.commit()
                return True
            except Exception as error:
                self.connect.rollback()
                raise error
            finally:
                cursor.close()

    def executemany(self, query: str = "", args=None):
        """
        call cursor.executemany
        :param query:
        :param args:
        :return:
        """
        if not isinstance(self.connect, Connect) or not self.connect.open:
            raise ValueError("connect is Connect and connect must be open")
        if not isinstance(query, str) or not len(query):
            raise ValueError(f"query:{query} must be string and not empty")
        with self.connect.cursor() as cursor:
            try:
                cursor.executemany(query=query, args=args)
                self.connect.commit()
                return cursor.rowcount
            except Exception as error:
                self.connect.rollback()
                raise error
            finally:
                cursor.close()

    def execute(self, query: str = "", args=None, cursor_func_or_prop: str = None):
        """
        call cursor.execute
        :param query:
        :param args:
        :param cursor_func_or_prop: return cursor func or prop
        :return:
        """
        if not isinstance(self.connect, Connect) or not self.connect.open:
            raise ValueError("connect is Connect and connect must be open")
        if not isinstance(query, str) or not len(query):
            raise ValueError(f"query:{query} must be string and not empty")
        with self.connect.cursor() as cursor:
            try:
                cursor.execute(query=query, args=args)
                self.connect.commit()
                if isinstance(cursor_func_or_prop, str) and len(cursor_func_or_prop):
                    if cursor_func_or_prop == CURSOR_FUNC_FETCHONE:
                        return cursor.fetchone()
                    if cursor_func_or_prop == CURSOR_FUNC_FETCHALL:
                        return cursor.fetchall()
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
                cursor.close()

    def rowcount(self, query: str = "", args=None):
        """
        call cursor.execute return cursor.rowcount
        :param query:
        :param args:
        :return:
        """
        return self.execute(query=query, args=args, cursor_func_or_prop=CURSOR_PROP_ROWCOUNT)

    def lastrowid(self, query: str = "", args=None):
        """
        call cursor.execute return cursor.lastrowid
        :param query:
        :param args:
        :return:
        """
        return self.execute(query=query, args=args, cursor_func_or_prop=CURSOR_PROP_LASTROWID)

    def description(self, query: str = "", args=None):
        """
        call cursor.execute return cursor.description
        :param query:
        :param args:
        :return:
        """
        return self.execute(query=query, args=args, cursor_func_or_prop=CURSOR_PROP_DESCRIPTION)

    def fetchone(self, query: str = "", args=None):
        """
        call cursor.execute return cursor.fetchone
        :param query:
        :param args:
        :return:
        """
        return self.execute(query=query, args=args, cursor_func_or_prop=CURSOR_FUNC_FETCHONE)

    def fetchall(self, query: str = "", args=None):
        """
        call cursor.execute return cursor.fetchall
        :param query:
        :param args:
        :return:
        """
        return self.execute(query=query, args=args, cursor_func_or_prop=CURSOR_FUNC_FETCHALL)
