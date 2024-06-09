"""
vulcan_utils/cache.py

This module provides a high-level interface for caching data using Redis. It encapsulates
the connection and basic operations such as setting, retrieving, deleting, and clearing data
in Redis databases. This is useful for applications that require fast data retrieval and 
effective data management using key-value storage.
"""

import json
from typing import Any, Optional

import redis
from redis.exceptions import RedisError

from vulcan_utils.encoder import Encoder


class Cache:
    """
    Manages caching operations via Redis. Provides methods to set, get, delete, and clear cache 
        data. The connection to the Redis server is established during class instantiation and 
        will raise a ConnectionError if unable to connect. All methods that interact with the 
        Redis server can raise a RedisError in case of operation failure.

    Attributes:
        redis (redis.Redis): Redis client instance connected to the specified server and database.

    Raises:
        ConnectionError: If the Redis server cannot be reached during initialization.
        RedisError: For any failures in cache operations.
    """

    def __init__(self, host="localhost", port=6379, db=0):
        """
        Initializes the Cache object with a Redis connection.
        Raises a ConnectionError if the Redis server cannot be reached.

        Args:
            host (str): The hostname of the Redis server.
            port (int): The port number on which the Redis server is running.
            db (int): The database number to connect to.
        """
        try:
            self.redis = redis.Redis(host=host, port=port, db=db)
            self.redis.ping()  # Try to ping the server to check connection
        except ConnectionError as e:
            raise ConnectionError(
                f"Failed to connect to Redis: {str(e)}"
            ) from e

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        """
        Stores a value in the cache, optionally setting an expiration time.

        Args:
            key (str): The key under which the value is stored.
            value (Any): The value to be stored.
            expire (Optional[int]): The expiration time in seconds. If not specified, the value 
                does not expire.

        Raises:
            RedisError: If the operation cannot be completed.
        """
        try:
            serialized_value = json.dumps(value, cls=Encoder)
            self.redis.set(key, serialized_value, ex=expire)
        except RedisError as e:
            raise RedisError(
                f"Failed to set key {key}: {str(e)}"
            ) from e

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieves a value from the cache.

        Args:
            key (str): The key for which the value is retrieved.

        Returns:
            Optional[Any]: The retrieved value or None if the key does not exist.

        Raises:
            RedisError: If the operation cannot be completed.
        """
        try:
            serialized_value = self.redis.get(key)
            if serialized_value is not None:
                return json.loads(serialized_value)
        except RedisError as e:
            raise RedisError(
                f"Failed to get key {key}: {str(e)}"
            ) from e
        return None

    def delete(self, key: str) -> None:
        """
        Deletes a specific key from the cache.

        Args:
            key (str): The key to be deleted.

        Raises:
            RedisError: If the operation cannot be completed.
        """
        try:
            self.redis.delete(key)
        except RedisError as e:
            raise RedisError(
                f"Failed to delete key {key}: {str(e)}"
            ) from e

    def clear(self) -> None:
        """
        Clears all keys and values from the current database.

        Raises:
            RedisError: If the operation cannot be completed.
        """
        try:
            self.redis.flushdb()
        except RedisError as e:
            raise RedisError(
                f"Failed to clear database: {str(e)}"
            ) from e
