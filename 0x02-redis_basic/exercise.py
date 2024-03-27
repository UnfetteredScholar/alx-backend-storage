#!/usr/bin/env python3
"""
Contains the Cache class definition
"""
from functools import wraps
from typing import Any, Callable, Union
from uuid import uuid4

import redis


def count_calls(method: Callable) -> Callable:
    """
    Create and return function that increments the count
    for that key every time the method is called
    and returns the value returned by the original method.

    key: __qualname__ of method
    """

    @wraps(method)
    def counter(self, *args, **kwargs) -> Any:
        """
        Invokes the given method after incrementing its count
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return counter


def call_history(method: Callable) -> Callable:
    """
    Store the history of inputs and outputs for a particular function
    everytime the original function will be called,
    we will add its input parameters to one list in redis,
    and store its output into another list.

    key: __qualname__ of method
    """

    @wraps(method)
    def tracker(self, *args, **kwargs) -> Any:
        """
        Invokes the given method after storing its input and output
        """
        if isinstance(self._redis, redis.Redis):
            res = method(self, *args, **kwargs)
            self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
            self._redis.rpush(f"{method.__qualname__}:outputs", str(res))
        return res

    return tracker


def replay(method: Callable) -> None:
    """Displays the call history of a function"""

    if method is None or not hasattr(method, "__self__"):
        return
    redis_db = getattr(method.__self__, "_redis", None)
    if not isinstance(redis_db, redis.Redis):
        return

    inputs = redis_db.lrange(f"{method.__qualname__}:inputs", 0, -1)
    outputs = redis_db.lrange(f"{method.__qualname__}:outputs", 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")

    for i, o in zip(inputs, outputs):
        i = i.decode("utf-8")
        o = o.decode("utf-8")
        print(f"{method.__qualname__}(*{i}) -> {o}")


class Cache:
    """Defines a cache"""

    def __init__(self) -> None:
        """Cache class constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a data value under a random key
        and returns the key
        """
        name = str(uuid4())
        self._redis.set(name, data)
        return name

    @call_history
    @count_calls
    def get(
        self, key: str, fn: Callable = None
    ) -> Union[str, bytes, int, float]:
        """
        Gets a value by its key from Redis db
        Converts the value if callable fn is not none
        """
        val = self._redis.get(key)
        if fn is not None and val is not None:
            val = fn(val)

        return val

    @call_history
    @count_calls
    def get_str(self, key: str) -> str:
        """Gets a value from redis and returns it as str"""
        return self.get(key, str)

    @call_history
    @count_calls
    def get_int(self, key: str) -> int:
        """Gets a value from redis and returns it as int"""
        return self.get(key, int)
