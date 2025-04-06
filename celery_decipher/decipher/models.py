from datetime import datetime
from typing import Literal, TypeAlias
from uuid import UUID

from pydantic import BaseModel

DocumentID: TypeAlias = UUID


class DecipherStartRequest(BaseModel):
    text: str


class DecipherStartResponse(BaseModel):
    source_text_id: DocumentID


class DecipherStatusResponse(BaseModel):
    source_text_id: DocumentID
    status: Literal["PENDING", "PROCESSING", "COMPLETED"]
    source_text: str
    deciphered_text: str | None = None
    started_at: datetime | None = None
    updated_at: datetime | None = None
