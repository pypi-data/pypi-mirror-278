#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
duckdb Class Library
-------------------------------------------------
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_database
=================================================
"""
from typing import Union

from addict import Dict
from duckdb import duckdb, DuckDBPyConnection


class Database(object):
    """
    Database Class
    """

    def __init__(
            self,
            connect_args: Union[tuple, list] = (),
            connect_kwargs: Union[dict, Dict] = Dict({}),
            install_extension_list: Union[list, tuple] = [],
            load_extension_list: Union[list, tuple] = [],
    ):
        """
        Database construct function
        :param connect_args: duckdb.connect args
        :param connect_kwargs: duckdb.connect kwargs
        :param install_extension_list: duckdb.DuckDBPyConnection install extension list
        :param load_extension_list: duckdb.DuckDBPyConnection load extension list
        """
        self._connect_args = connect_args
        self._connect_kwargs = connect_kwargs
        self._install_extension_list = install_extension_list
        self._load_extension_list = load_extension_list
        self._connect: DuckDBPyConnection = None

    @property
    def connect_args(self) -> Union[tuple, list]:
        """
        duckdb.connect args
        :return:
        """
        return self._connect_args

    @connect_args.setter
    def connect_args(self, value: Union[tuple, list]):
        """
        dduckdb.connect args
        :param value:
        :return:
        """
        self._connect_args = value

    @property
    def connect_kwargs(self) -> Union[dict, Dict]:
        """
        duckdb.connect kwargs
        :return:
        """
        return self._connect_kwargs

    @connect_kwargs.setter
    def connect_kwargs(self, value: Union[dict, Dict]):
        """
        duckdb.connect kwargs
        :param value:
        :return:
        """
        self._connect_kwargs = value

    @property
    def install_extension_list(self) -> list:
        """
        duckdb.DuckDBPyConnection install extension list
        :return:
        """
        return self._install_extension_list

    @install_extension_list.setter
    def install_extension_list(self, value: list = []):
        """
        duckdb.DuckDBPyConnection install extension list
        :param value:
        :return:
        """
        self._install_extension_list = value

    @property
    def load_extension_list(self) -> list:
        """
        duckdb.DuckDBPyConnection load extension list
        :return:
        """
        return self._load_extension_list

    @load_extension_list.setter
    def load_extension_list(self, value: list = []):
        """
        duckdb.DuckDBPyConnection load extension list
        :param value:
        :return:
        """
        self._load_extension_list = value

    @property
    def connect(self) -> DuckDBPyConnection:
        """
        duckdb.DuckDBPyConnection
        :return:
        """
        return self._connect

    def open_connect(self, install_extension_list=[], load_extension_list=[]) -> bool:
        """
        open duckdb.DuckDBPyConnection
        :param install_extension_list: duckdb.DuckDBPyConnection install extension list
        :param load_extension_list: duckdb.DuckDBPyConnection load extension list
        :return:
        """
        if not isinstance(install_extension_list, list):
            install_extension_list = []
        if not isinstance(load_extension_list, list):
            load_extension_list = []
        self.connect_kwargs = Dict(self.connect_kwargs)
        connect: DuckDBPyConnection = duckdb.connect(*self.connect_args, **self.connect_kwargs.to_dict())
        for extension in self.install_extension_list + install_extension_list:
            connect.install_extension(extension)
        for extension in self.load_extension_list + load_extension_list:
            connect.load_extension(extension)
        return True

    def close_connect(self) -> bool:
        """
        close open duckdb.DuckDBPyConnection
        :return:
        """
        if isinstance(self.connect, DuckDBPyConnection):
            self.connect.close()
            return True
        return False
