#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import functools
import sqlite3


def open_connect(*args, **kwargs) -> sqlite3.Connection:
    """
    open Connect
    :param args:
    :param kwargs:
    :return: Connect
    """
    connect = sqlite3.connect(*args, **kwargs)
    connect.row_factory = sqlite3.Row
    return connect


def close_connect(connect: sqlite3.Connection = None) -> bool:
    """
    close Connect
    :param args:
    :param kwargs:
    :return: Connect
    """
    if isinstance(connect, sqlite3.Connection):
        connect.close()
        return True
    return False


def execute(connect: sqlite3.Connection = None, sql: str = "", parameters=()) -> tuple:
    if not isinstance(connect, sqlite3.Connection):
        raise ValueError("connect must be sqlite3.Connection")
    if not isinstance(sql, str) or not len(sql):
        raise ValueError("sql must be string and not empty")
    if not parameters:
        parameters = ()
    try:
        cursor = connect.cursor()
        cursor.execute(sql, parameters)
        connect.commit()
        return cursor.rowcount, cursor.lastrowid
    except Exception as error:
        raise error
    finally:
        if isinstance(cursor, sqlite3.Cursor):
            cursor.close()


def executemany(connect: sqlite3.Connection = None, sql: str = "", seq_of_parameters=None) -> int:
    if not isinstance(connect, sqlite3.Connection):
        raise ValueError("connect must be sqlite3.Connection")
    if not isinstance(sql, str) or not len(sql):
        raise ValueError("sql must be string and not empty")
    try:
        cursor = connect.cursor()
        cursor.executemany(sql, seq_of_parameters)
        connect.commit()
        return cursor.rowcount
    except Exception as error:
        raise error
    finally:
        if isinstance(cursor, sqlite3.Cursor):
            cursor.close()


def executescript(connect: sqlite3.Connection = None, sql_script: str = "") -> int:
    if not isinstance(connect, sqlite3.Connection):
        raise ValueError("connect must be sqlite3.Connection")
    if not isinstance(sql_script, str) or not len(sql_script):
        raise ValueError("sql_script must be string and not empty")
    try:
        cursor = connect.cursor()
        connect.executescript(sql_script)
        connect.commit()
        return cursor.rowcount
    except Exception as error:
        connect.rollback()
        raise error
    finally:
        if isinstance(cursor, sqlite3.Cursor):
            cursor.close()


def fetchone(connect: sqlite3.Connection = None, sql: str = "", parameters=()):
    if not isinstance(connect, sqlite3.Connection):
        raise ValueError("connect must be sqlite3.Connection")
    if not isinstance(sql, str) or not len(sql):
        raise ValueError("sql must be string and not empty")
    if not parameters:
        parameters = ()
    try:
        cursor = connect.cursor()
        cursor.execute(sql, parameters)
        return cursor.fetchone()
    except Exception as error:
        raise error
    finally:
        if isinstance(cursor, sqlite3.Cursor):
            cursor.close()


def fetchall(connect: sqlite3.Connection = None, sql: str = "", parameters=()):
    if not isinstance(connect, sqlite3.Connection):
        raise ValueError("connect must be sqlite3.Connection")
    if not isinstance(sql, str) or not len(sql):
        raise ValueError("sql must be string and not empty")
    if not parameters:
        parameters = ()
    try:
        cursor = connect.cursor()
        cursor.execute(sql, parameters)
        return cursor.fetchall()
    except Exception as error:
        raise error
    finally:
        if isinstance(cursor, sqlite3.Cursor):
            cursor.close()
