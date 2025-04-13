from typing import Literal as TLiteral
from typing import TypeAlias

from psycopg import Cursor
from psycopg.rows import DictRow
from psycopg.sql import SQL, Literal, Placeholder
from psycopg.types.json import Jsonb

from celery_decipher.decipher.cipher import CandidateID, CipherMap
from celery_decipher.decipher.models import DocumentID

DecipherStatus: TypeAlias = TLiteral["PENDING", "PROCESSING", "COMPLETED"]


def insert_source_text(cursor: Cursor[DictRow], text: str) -> DocumentID | None:
    stmt = SQL(
        """
        INSERT INTO decipher_sources (text)
        VALUES ({text})
        RETURNING source_text_id
        """
    ).format(text=text)
    result = cursor.execute(stmt).fetchone()
    return result["source_text_id"] if result is not None else None


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


def insert_candidates(
    cursor: Cursor[DictRow], source_text_id: DocumentID, candidates: list[CipherMap]
) -> None:
    placeholders = SQL(", ").join(
        [SQL("({})").format(SQL(", ").join([Placeholder()] * 2))] * len(candidates)
    )
    params = [
        item for candidate in candidates for item in (source_text_id, Jsonb(candidate))
    ]
    stmt = SQL(
        """
        INSERT INTO candidates (source_text_id, cipher_map)
        VALUES {placeholders}
        """
    ).format(placeholders=placeholders)
    cursor.execute(stmt, params)


def get_candidates(
    cursor: Cursor[DictRow], source_text_id: DocumentID
) -> list[tuple[CandidateID, CipherMap]] | None:
    stmt = SQL(
        """
        SELECT candidate_id, cipher_map FROM candidates
        WHERE source_text_id = {source_text_id}
        """
    ).format(source_text_id=Literal(source_text_id))
    results = cursor.execute(stmt)
    return (
        [(result["candidate_id"], result["cipher_map"]) for result in results]
        if results
        else None
    )


def get_status(
    cursor: Cursor[DictRow],
    source_text_id: DocumentID,
) -> dict[str, str] | None:
    query = SQL(
        """
        SELECT source_text_id, ss.text AS source_text, status, started_at, updated_at, bcs.cipher_map, bcs.score, bcs.deciphered_text
        FROM decipher_status
        JOIN decipher_sources ss USING(source_text_id)
        LEFT JOIN best_candidates bcs USING(source_text_id)
        WHERE source_text_id = {source_text_id}
        """
    ).format(source_text_id=Literal(source_text_id))
    result = cursor.execute(query).fetchone()
    return result if result else None

