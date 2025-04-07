from celery import Celery

from celery_decipher.settings import settings

app = Celery(
    "celery_decipher",
    broker=settings.celery_broker_url,
    backend=settings.celery_backend_url,
)

app.autodiscover_tasks()
