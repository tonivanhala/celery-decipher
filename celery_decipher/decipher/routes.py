from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from psycopg import Cursor
from psycopg.rows import DictRow

from celery_decipher.celery.tasks import decipher_text
from celery_decipher.db import db_cursor
from celery_decipher.decipher.db import (
    get_source_text,
    get_status,
    insert_source_text,
)
from celery_decipher.decipher.models import (
    DecipherStartRequest,
    DecipherStartResponse,
    DecipherStatusResponse,
)

router = APIRouter(prefix="/decipher")


@router.post("/", response_model=DecipherStartResponse)
async def decipher(
    cursor: Annotated[Cursor[DictRow], Depends(db_cursor)],
    request: DecipherStartRequest,
) -> DecipherStartResponse:
    source_text_id = insert_source_text(cursor, request.text)
    if source_text_id is None:
        raise Exception("Failed to start deciphering")
    decipher_text().apply_async(args=(source_text_id,))
    return DecipherStartResponse(source_text_id=source_text_id)


@router.get("/{source_text_id}", response_model=DecipherStatusResponse)
async def status(
    cursor: Annotated[Cursor[DictRow], Depends(db_cursor)],
    source_text_id: UUID,
) -> DecipherStatusResponse:
    decipher_status = get_status(cursor, source_text_id)
    if decipher_status is None:
        text = get_source_text(cursor, source_text_id)
        if text is None:
            raise Exception(f"Source text with id {source_text_id} not found")
        return DecipherStatusResponse(
            source_text_id=source_text_id,
            status="PENDING",
            source_text=text,
        )
    return DecipherStatusResponse.model_validate(decipher_status)
