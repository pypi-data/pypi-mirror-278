#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import functools
from typing import List

import pymysql
from pymysql import Connect
from pymysql.cursors import DictCursor


def open_connect(*args, **kwargs) -> Connect:
    """
    open Connect
    :param args: Connect(*args, **kwargs)
    :param kwargs: Connect(*args, **kwargs)
    :return: Connect
    """
    if isinstance(kwargs, dict) and not "cursorclass" in kwargs.keys():
        kwargs["cursorclass"] = DictCursor
    return Connect(*args, **kwargs)


def close_connect(connect: Connect = None) -> bool:
    """
    close Connect
    :param args:
    :param kwargs:
    :return: Connect
    """
    if isinstance(connect, Connect) and connect.open:
        connect.close()
        return True
    return False


def execute(connect: Connect = None, *args, **kwargs) -> tuple:
    if not isinstance(connect, Connect) or not connect.open:
        raise ValueError("connect is Connect and connect must be open")
    with connect.cursor() as cursor:
        try:
            cursor.execute(*args, **kwargs)
            connect.commit()
            return True, cursor.rowcount, cursor.lastrowid
        except Exception as error:
            raise error
        finally:
            if isinstance(cursor, pymysql.cursors.Cursor):
                cursor.close()


def executemany(connect: Connect = None, *args, **kwargs) -> tuple:
    if not isinstance(connect, Connect) or not connect.open:
        raise ValueError("connect is Connect and connect must be open")
    with connect.cursor() as cursor:
        try:
            cursor.executemany(*args, **kwargs)
            connect.commit()
            return True, cursor.rowcount
        except Exception as error:
            raise error
        finally:
            if isinstance(cursor, pymysql.cursors.Cursor):
                cursor.close()


def execute_transaction(connect: Connect = None, queries: list = []) -> tuple:
    if not isinstance(connect, Connect) or not connect.open:
        raise ValueError("connect is Connect and connect must be open")
    with connect.cursor() as cursor:
        try:
            connect.begin()
            for query in queries:
                if isinstance(query, tuple):
                    cursor.execute(*query)
                if isinstance(query, dict):
                    cursor.execute(**query)
                if isinstance(query, str):
                    cursor.execute(query)
            connect.commit()
            return True, cursor.rowcount
        except Exception as error:
            connect.rollback()
            raise error
        finally:
            if isinstance(cursor, pymysql.cursors.Cursor):
                cursor.close()


def fetchone(connect: Connect = None, *args, **kwargs) -> tuple:
    if not isinstance(connect, Connect) or not connect.open:
        raise ValueError("connect is Connect and connect must be open")
    with connect.cursor() as cursor:
        try:
            cursor.execute(*args, **kwargs)
            return True, cursor.fetchone()
        except Exception as error:
            raise error
        finally:
            if isinstance(cursor, pymysql.cursors.Cursor):
                cursor.close()


def fetchall(connect: Connect = None, *args, **kwargs) -> tuple:
    if not isinstance(connect, Connect) or not connect.open:
        raise ValueError("connect is Connect and connect must be open")
    with connect.cursor() as cursor:
        try:
            cursor.execute(*args, **kwargs)
            return True, cursor.fetchall()
        except Exception as error:
            raise error
        finally:
            if isinstance(cursor, pymysql.cursors.Cursor):
                cursor.close()
