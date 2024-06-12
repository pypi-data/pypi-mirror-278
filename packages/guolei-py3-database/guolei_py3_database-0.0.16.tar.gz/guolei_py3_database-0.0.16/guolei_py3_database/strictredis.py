#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import functools
import types

import redis


def open_connect(*args, **kwargs) -> redis.StrictRedis:
    return redis.StrictRedis(*args, **kwargs)


def close_connect(connect: redis.StrictRedis = None) -> bool:
    if isinstance(connect, redis.StrictRedis):
        connect.close()
        return True
    return False


def execute(connect: redis.StrictRedis = None, method: str = "", *args, **kwargs):
    if not isinstance(method, str) or not len(method) or not hasattr(connect, method):
        raise AttributeError(f"method must str and not empty")
    if not hasattr(connect, method):
        raise AttributeError(f"{method} is not a valid function")
    func = getattr(connect, method)
    if not isinstance(func, types.FunctionType):
        raise AttributeError(f"{method} is not a valid function")
    return func(*args, **kwargs)
