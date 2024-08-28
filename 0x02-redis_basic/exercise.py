#!/usr/bin/env python3
"""
Redis basic.
"""
from typing import Union, Callable, Optional
from functools import wraps
import redis
import uuid


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a particular function."""
    method_key = method.__qualname__
    inputs, outputs = f"{method_key}:inputs", f"{method_key}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result

    return wrapper


def count_calls(method: Callable) -> Callable:
    """Increments the count for that key every time the method is called."""
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)

    return wrapper


def replay(method: Callable) -> None:
    """Displays the history of calls of a particular function."""
    method_key = method.__qualname__
    inputs, outputs = f"{method_key}:inputs", f"{method_key}:outputs"
    redis_client = method.__self__._redis
    method_count = redis_client.get(method_key).decode('utf-8')
    
    print(f"{method_key} was called {method_count} times:")
    IOTuple = zip(redis_client.lrange(inputs, 0, -1), redis_client.lrange(outputs, 0, -1))
    
    for inp, outp in IOTuple:
        attr, data = inp.decode("utf-8"), outp.decode("utf-8")
        print(f"{method_key}(*{attr}) -> {data}")


class Cache:
    """Cache class to handle Redis operations."""
    
    def __init__(self):
        """Stores an instance of the Redis client."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores a data argument and returns a unique key."""
        key = str(uuid.uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, None]:
        """Retrieves a value by key, converting it using an optional callable."""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, data: bytes) -> str:
        """Returns the string value of decoded bytes."""
        return data.decode('utf-8', 'strict')

    def get_int(self, data: bytes) -> int:
        """Returns the integer value of decoded bytes."""
        return int(data)

