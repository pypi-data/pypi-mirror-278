from ...common._redis_client import RedisClient
import redis
import os

def save_progress(
    file_key: str,
    progress: str,
) -> None:
    client = RedisClient.get_instance()
    client.set(
        name=f"pms:encoder:progress:{file_key}",
        value=progress,
        ex=1800
    )