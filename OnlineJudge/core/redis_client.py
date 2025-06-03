import redis
from core.config import settings

"""Redis client setup for the Online Judge application."""

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)