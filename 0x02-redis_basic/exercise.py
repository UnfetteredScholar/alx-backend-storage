#!/usr/bin/env python3
from typing import Union
from uuid import uuid4

import redis

"""
Contains the Cache class definition
"""


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
