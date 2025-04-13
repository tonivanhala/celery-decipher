from contextlib import contextmanager
from typing import Iterable, Iterator

from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
from psycopg import Connection, Cursor
from psycopg.rows import DictRow, dict_row
from psycopg_pool import ConnectionPool

from celery_decipher.settings import settings
from celery_decipher.tracing import get_tracer


def configure_connection(conn: Connection[DictRow]) -> None:
    PsycopgInstrumentor.instrument_connection(conn, tracer_provider=get_tracer())  # type: ignore


db_pool = ConnectionPool(
    conninfo=settings.pg_connection_string,
    open=False,
    configure=configure_connection,
)


def db_cursor() -> Iterable[Cursor[DictRow]]:
    with db_pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            yield cur


@contextmanager
def get_cursor() -> Iterator[Cursor[DictRow]]:
    with db_pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            yield cur
