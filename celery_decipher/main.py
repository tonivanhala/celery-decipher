from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.starlette import StarletteInstrumentor
from starlette.requests import Request

from celery_decipher.celery.app import app as celery_app
from celery_decipher.db import db_pool
from celery_decipher.decipher.routes import router as decipher_routes
from celery_decipher.tracing import initialize_tracer

celery_app.set_default()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    db_pool.open()
    yield
    db_pool.close()


app = FastAPI(lifespan=lifespan)
app.include_router(decipher_routes)

trace_provider = initialize_tracer("FastAPI")
LoggingInstrumentor().instrument(set_logging_format=True)
StarletteInstrumentor.instrument_app(app, tracer_provider=trace_provider)
FastAPIInstrumentor.instrument_app(app, tracer_provider=trace_provider)


@app.get("/healthz", response_class=PlainTextResponse)
async def health(_request: Request) -> str:
    return "OK"
