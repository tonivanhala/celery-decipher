from datetime import datetime
from typing import Literal, TypeAlias
from uuid import UUID

from pydantic import BaseModel

DocumentID: TypeAlias = UUID
WordLength: TypeAlias = int


class DecipherStartRequest(BaseModel):
    text: str


class DecipherStartResponse(BaseModel):
    source_text_id: DocumentID


class DecipherStatusResponse(BaseModel):
    source_text_id: DocumentID
    status: Literal["PENDING", "PROCESSING", "COMPLETED"]
    source_text: str
    cipher_map: dict[str, str] | None = None
    score: float | None = None
    deciphered_text: str | None = None
    started_at: datetime | None = None
    updated_at: datetime | None = None
