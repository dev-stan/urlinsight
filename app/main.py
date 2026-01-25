from app.core import config
from fastapi import FastAPI, Request, HTTPException
from app.api.routers import links, redirect
from app.db.database import engine, Base
from contextlib import asynccontextmanager
import time
import redis.asyncio as redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield # needed for context manager!!

app = FastAPI(lifespan=lifespan)
app.include_router(links.router)
app.include_router(redirect.router)

REDIS_HOST = "localhost"
REDIS_PORT = 6379
BUCKET_MS = 100
LIMIT = 5

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    requester = request.client.host
    
    now_ms = int(time.time() * 1000)
    bucket_id = now_ms // BUCKET_MS

    redis_key = f"rl:{requester}:{bucket_id}"

    count = await redis_client.incr(redis_key)
    if count == 1:
        await redis_client.pexpire(redis_key, BUCKET_MS)

    if count > LIMIT:
        raise HTTPException(status_code=429, detail="Too Many Requests")

    response = await call_next(request)
    return response