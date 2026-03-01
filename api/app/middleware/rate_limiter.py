import time

import redis.asyncio as redis
from fastapi import Request

REDIS_HOST = "localhost"
REDIS_PORT = 6379
BUCKET_MS = 1000
LIMIT = 5

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


async def rate_limiter_handler(request: Request, call_next):
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

    response = await call_next(request)
    return response
