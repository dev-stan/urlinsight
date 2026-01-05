from fastapi import FastAPI
from routers import links, redirect
from database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield # needed for context manager!!

app = FastAPI(lifespan=lifespan)
app.include_router(links.router)
app.include_router(redirect.router)
