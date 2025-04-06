from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.requests import Request

from celery_decipher.db import db_pool
from celery_decipher.decipher.routes import router as decipher_routes


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    db_pool.open()
    yield
    db_pool.close()


app = FastAPI(lifespan=lifespan)
app.include_router(decipher_routes)


@app.get("/healthz", response_class=PlainTextResponse)
async def health(_request: Request) -> str:
    return "OK"
