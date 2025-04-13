from uuid import UUID

from celery import chain, chord, shared_task

from celery_decipher.db import get_cursor
from celery_decipher.decipher.solver import initial_guess as make_initial_guess


def decipher_text() -> chain:
    return chain(
        initial_guess.s(),
    )


@shared_task
def initial_guess(source_text_id: UUID) -> UUID:
    with get_cursor() as cur:
        make_initial_guess(cur, source_text_id)
    return source_text_id
