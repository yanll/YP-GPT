import os
import pickle
import redis
from redis.exceptions import ConnectionError
from dbgpt.util.sutil import reidspwd


class RedisClient:
    PRIFIX = "/YP-GPT_"

    def __init__(self, host=os.getenv("REDIS_HOST"), port=6379, db=0, max_connections=20):
        self.host = host
        self.port = port
        self.db = db
        self.max_connections = max_connections
        self.password = reidspwd()
        self.pool = None
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.pool = redis.ConnectionPool(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                max_connections=self.max_connections
            )
            self.connection = redis.Redis(connection_pool=self.pool)
        except ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")
            raise

    def set(self, key, value, expire):
        """单位：秒"""
        try:
            serialized_value = pickle.dumps(value)
            self.connection.setex(self.PRIFIX + key, expire, serialized_value)
        except ConnectionError as e:
            print(f"Failed to set value in Redis: {e}")
            raise

    def get(self, key):
        try:
            serialized_value = self.connection.get(self.PRIFIX + key)
            if serialized_value is not None:
                return pickle.loads(serialized_value)
            return None
        except ConnectionError as e:
            print(f"Failed to get value from Redis: {e}")
            raise

    def exists(self, key):
        try:
            return self.connection.exists(self.PRIFIX + key)
        except ConnectionError as e:
            print(f"Failed to get value from Redis: {e}")
            raise

    def expire(self, key, expire):
        """单位：秒"""
        try:
            self.connection.expire(self.PRIFIX + key, expire)
        except ConnectionError as e:
            print(f"Failed to set expiration time for key in Redis: {e}")
            raise

    def delete(self, key):
        try:
            self.connection.delete(self.PRIFIX + key)
        except ConnectionError as e:
            print(f"Failed to delete value from Redis: {e}")
            raise

    def disconnect(self):
        try:
            self.connection.close()
        except ConnectionError as e:
            print(f"Failed to disconnect from Redis: {e}")
            raise

#
# if __name__ == '__main__':
#     key = "test"
#     cli = RedisClient()
#     print(cli.exists(key))
#     cli.set(key, '123456', 60)
#     print(cli.exists(key))
#     print(cli.get(key))
#     cli.delete(key)
#     print(cli.get(key))
