from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import links, redirect
from app.db.database import Base, engine
from app.middleware import rate_limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield  # needed for context manager!!


app = FastAPI(lifespan=lifespan)

app.middleware("http")(rate_limiter.rate_limiter_handler)

app.include_router(links.router)
app.include_router(redirect.router)
