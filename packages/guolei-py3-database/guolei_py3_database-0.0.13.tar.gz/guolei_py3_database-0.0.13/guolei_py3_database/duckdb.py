#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from typing import Union

from duckdb import duckdb, DuckDBPyConnection


def open_connect(
        install_extension_list: Union[list, tuple] = [],
        load_extension_list: Union[list, tuple] = [],
        **connect_kwargs
) -> DuckDBPyConnection:
    """
    open connect
    :param install_extension_list: loop run connection.install_extension(install_extension_list[i])
    :param load_extension_list: loop run connection.load_extension(load_extension_list[i])
    :param connect_kwargs: duckdb.connect(**connect_kwargs)
    :return: DuckDBPyConnection
    """
    connect: DuckDBPyConnection = duckdb.connect(**connect_kwargs)
    for extension in install_extension_list:
        connect.install_extension(extension)
    for extension in load_extension_list:
        connect.load_extension(extension)
    return connect


def close_connect(connect: DuckDBPyConnection = None) -> bool:
    """
    close connect
    :param connect: DuckDBPyConnection
    :return:
    """
    if isinstance(connect, DuckDBPyConnection):
        connect.close()
        return True
    return False


def execute(connection: DuckDBPyConnection, *args, **kwargs) -> DuckDBPyConnection:
    """
    execute
    :param connection: DuckDBPyConnection
    :param args: connection.execute(*args, **kwargs)
    :param kwargs: connection.execute(*args, **kwargs)
    :return: DuckDBPyConnection
    """
    if not isinstance(connection, DuckDBPyConnection):
        raise ValueError('connection must be DuckDBPyConnection')
    return connection.execute(*args, **kwargs)
