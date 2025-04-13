from celery import Celery

from celery_decipher.db import db_pool
from celery_decipher.settings import settings

db_pool.open()

app = Celery(
    "celery_decipher",
    broker=settings.celery_broker_url,
    backend=settings.celery_backend_url,
)

app.autodiscover_tasks(["celery_decipher.celery.tasks"])
