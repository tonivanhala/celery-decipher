from typing import Iterable

from psycopg import Cursor
from psycopg.rows import DictRow, dict_row
from psycopg_pool import ConnectionPool

from celery_decipher.settings import settings

db_pool = ConnectionPool(
    conninfo=settings.pg_connection_string,
    open=False,
)


def db_cursor() -> Iterable[Cursor[DictRow]]:
    with db_pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            yield cur
