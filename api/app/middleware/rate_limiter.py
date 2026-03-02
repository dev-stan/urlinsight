import time

import redis.asyncio as redis
from fastapi import Request

from app.core.config import settings

BUCKET_MS = 1000
LIMIT = 5

redis_client = None
if settings.redis_url:
    redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


async def rate_limiter_handler(request: Request, call_next):
    if redis_client is None:
        return await call_next(request)

    try:
        requester = request.client.host

        now_ms = int(time.time() * 1000)
        bucket_id = now_ms // BUCKET_MS
        redis_key = f"rl:{requester}:{bucket_id}"

        count = await redis_client.incr(redis_key)
        if count == 1:
            await redis_client.pexpire(redis_key, BUCKET_MS)

        if count > LIMIT:
            from fastapi.responses import JSONResponse

            return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})
    except Exception:
        pass

    response = await call_next(request)
    return response
