import redis
import os

class RedisClient:
    _instance = None
    
    @staticmethod
    def get_instance():
        if RedisClient._instance is None:
            RedisClient._instance = redis.StrictRedis(
                host=os.getenv("REDIS_HOST"),
                password=os.getenv("REDIS_PASSWORD"),
            )
        
        return RedisClient._instance