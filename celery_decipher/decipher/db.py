from psycopg import Cursor
from psycopg.rows import DictRow
from psycopg.sql import SQL, Literal

from celery_decipher.decipher.models import DocumentID


def insert_source_text(cursor: Cursor[DictRow], text: str) -> DocumentID:
    stmt = SQL(
        """
        INSERT INTO decipher_sources (text)
        VALUES ({text})
        RETURNING source_text_id
        """
    ).format(text=text)
    result = cursor.execute(stmt)
    return result.fetchone()["source_text_id"]


def get_source_text(cursor: Cursor[DictRow], source_text_id: DocumentID) -> str | None:
    query = SQL(
        """
        SELECT text
        FROM decipher_sources
        WHERE source_text_id = {source_text_id}
        """
    ).format(source_text_id=Literal(source_text_id))
    result = cursor.execute(query).fetchone()
    return result["text"] if result else None


def get_status(
    cursor: Cursor[DictRow],
    source_text_id: DocumentID,
) -> str | None:
    query = SQL(
        """
        SELECT source_text_id, status, started_at, updated_at
        FROM decipher_status
        JOIN decipher_sources USING(source_text_id)
        WHERE source_text_id = {source_text_id}
        """
    ).format(source_text_id=Literal(source_text_id))
    result = cursor.execute(query).fetchone()
    return result if result else None
