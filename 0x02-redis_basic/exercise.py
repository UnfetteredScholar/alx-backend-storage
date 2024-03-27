#!/usr/bin/env python3
"""
Contains the Cache class definition
"""
from typing import Callable, Union
from uuid import uuid4

import redis


class Cache:
    """Defines a cache"""

    def __init__(self) -> None:
        """Cache class constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a data value under a random key
        and returns the key
        """
        name = str(uuid4())
        self._redis.set(name, data)
        return name

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

    def get_str(self, key: str) -> str:
        """Gets a value from redis and returns it as str"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Gets a value from redis and returns it as int"""
        return self.get(key, int)
