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


def execute(connect: sqlite3.Connection = None, *args, **kwargs) -> tuple:
    if not isinstance(connect, sqlite3.Connection):
        raise ValueError("connect must be sqlite3.Connection")
    try:
        cursor = connect.cursor()
        cursor.execute(*args, **kwargs)
        connect.commit()
        return True, cursor.rowcount, cursor.lastrowid
    except Exception as error:
        raise error
    finally:
        if isinstance(cursor, sqlite3.Cursor):
            cursor.close()


def executemany(connect: sqlite3.Connection = None, *args, **kwargs) -> tuple:
    if not isinstance(connect, sqlite3.Connection):
        raise ValueError("connect must be sqlite3.Connection")
    try:
        cursor = connect.cursor()
        cursor.execute(*args, **kwargs)
        connect.commit()
        return True, cursor.rowcount
    except Exception as error:
        raise error
    finally:
        if isinstance(cursor, sqlite3.Cursor):
            cursor.close()


def execute_transaction(connect: sqlite3.Connection = None, queries: list = []) -> tuple:
    if not isinstance(connect, sqlite3.Connection):
        raise ValueError("connect must be sqlite3.Connection")
    try:
        cursor = connect.cursor()
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
        if isinstance(cursor, sqlite3.Cursor):
            cursor.close()


def fetchone(connect: sqlite3.Connection = None, *args, **kwargs) -> tuple:
    if not isinstance(connect, sqlite3.Connection):
        raise ValueError("connect must be sqlite3.Connection")
    try:
        cursor = connect.cursor()
        cursor.execute(*args, **kwargs)
        return True, cursor.fetchone()
    except Exception as error:
        raise error
    finally:
        if isinstance(cursor, sqlite3.Cursor):
            cursor.close()


def fetchall(connect: sqlite3.Connection = None, *args, **kwargs) -> tuple:
    if not isinstance(connect, sqlite3.Connection):
        raise ValueError("connect must be sqlite3.Connection")
    try:
        cursor = connect.cursor()
        cursor.execute(*args, **kwargs)
        return True, cursor.fetchall()
    except Exception as error:
        raise error
    finally:
        if isinstance(cursor, sqlite3.Cursor):
            cursor.close()
