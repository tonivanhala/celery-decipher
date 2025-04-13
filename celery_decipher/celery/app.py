from celery import Celery
from celery.signals import worker_process_init
from opentelemetry.instrumentation.celery import CeleryInstrumentor

from celery_decipher.db import db_pool
from celery_decipher.settings import settings
from celery_decipher.tracing import initialize_tracer

db_pool.open()

app = Celery(
    "celery_decipher",
    broker=settings.celery_broker_url,
    backend=settings.celery_backend_url,
)

app.autodiscover_tasks(["celery_decipher.celery.tasks"])

tracer_provider = initialize_tracer("CeleryDecipher")


@worker_process_init.connect(weak=False)
def init_celery_tracing(*args, **kwargs) -> None:
    CeleryInstrumentor().instrument(tracer_provider=tracer_provider)
