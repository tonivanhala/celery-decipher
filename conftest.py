from typing import Iterable

import httpx
import psycopg
import psycopg.rows
import pytest
from psycopg_pool import ConnectionPool

from celery_decipher import db, settings
from celery_decipher.settings import Settings


class TestSettings(Settings):
    pg_connection_string: str = (
        "postgresql://coo:chief-of-operations@localhost:5432/operational_test"
    )


settings.settings = TestSettings()
testdb_pool = ConnectionPool(
    conninfo=settings.settings.pg_connection_string,
    open=True,
)
db.db_pool = testdb_pool


DB_TABLES = [
    "decipher_sources",
    "decipher_status",
]


def truncate_tables(conn: psycopg.Connection) -> None:
    with conn.cursor() as cursor:
        cursor.execute(f"TRUNCATE TABLE {', '.join(DB_TABLES)} CASCADE;")


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