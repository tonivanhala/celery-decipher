from uuid import UUID

from celery import chain, shared_task

from celery_decipher.db import get_cursor
from celery_decipher.decipher.solver import initial_guess as make_initial_guess
from celery_decipher.decipher.solver import run_iteration


def decipher_text() -> chain:
    return chain(
        initial_guess.s(),
        iterate_solver.s(),
    )


@shared_task()
def initial_guess(source_text_id: UUID) -> UUID:
    with get_cursor() as cur:
        make_initial_guess(cur, source_text_id)
    return source_text_id


@shared_task()
def iterate_solver(source_text_id: UUID, iteration_count: int = 1) -> UUID:
    with get_cursor() as cur:
        trigger_iteration = run_iteration(cur, source_text_id, iteration_count)
        if trigger_iteration:
            iterate_solver.apply_async(args=(source_text_id, iteration_count + 1))
    return source_text_id
