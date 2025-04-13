from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_connection_string: str = (
        "postgresql://coo:chief-of-operations@localhost:5432/operational"
    )
    celery_backend_url: str = (
        "db+postgresql+psycopg://celery:celery@localhost:5432/celery"
    )
    celery_broker_url: str = (
        "amqp://op_user:OPERATIONAL@localhost:5672/operational_vhost"
    )
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"


settings = Settings()
