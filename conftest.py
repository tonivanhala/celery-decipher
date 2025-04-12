from typing import Iterable

import httpx
import psycopg
import psycopg.rows
from psycopg.sql import SQL, Identifier
import pytest
from psycopg_pool import ConnectionPool

from celery_decipher import db, settings
from celery_decipher.settings import Settings


class TestSettings(Settings):
    pg_connection_string: str = (
        "postgresql://coo:chief-of-operations@localhost:5432/operational_test"
    )
    celery_backend_url: str = "db+postgresql://celery_test:celery_test@localhost:5432/celery_test"
    celery_broker_url: str = (
        "amqp://test_user:TEST@localhost:5672/test_vhost"
    )


settings.settings = TestSettings()
testdb_pool = ConnectionPool(
    conninfo=settings.settings.pg_connection_string,
    open=True,
)
db.db_pool = testdb_pool


DB_TABLES = [
    "candidates",
    "decipher_sources",
    "decipher_status",
]


def truncate_tables(conn: psycopg.Connection) -> None:
    tables = SQL(", ").join([Identifier(table_name) for table_name in DB_TABLES])
    with conn.cursor() as cursor:
        query = SQL("TRUNCATE TABLE {tables} CASCADE;").format(tables=tables)
        cursor.execute(query)


@pytest.fixture()
def testdb_cursor() -> Iterable[psycopg.Cursor[psycopg.rows.DictRow]]:
    with testdb_pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            try:
                yield cur
            finally:
                truncate_tables(conn)


@pytest.fixture(scope="session")
def _http_client() -> Iterable[httpx.Client]:
    from fastapi.testclient import TestClient

    from celery_decipher.main import app

    with TestClient(app) as client:
        yield client
        with testdb_pool.connection() as conn:
            truncate_tables(conn)


@pytest.fixture
def http_client(_http_client: httpx.Client) -> Iterable[httpx.Client]:
    with testdb_pool.connection() as conn:
        truncate_tables(conn)
    yield _http_client