from celery_decipher.decipher.db import (
    get_candidates,
    get_source_text,
    insert_source_text,
)
from celery_decipher.decipher.solver import (
    POPULATION_SIZE,
    initial_guess,
)


def test_insert(testdb_cursor):
    text = "Smoky smoke test"
    source_text_id = insert_source_text(testdb_cursor, text)
    assert source_text_id is not None
    retrieved_text = get_source_text(testdb_cursor, source_text_id)
    assert retrieved_text == text


def test_initial_guess(testdb_cursor):
    text = "Smoky smoke test"
    source_text_id = insert_source_text(testdb_cursor, text)
    initial_guess(testdb_cursor, source_text_id)
    candidates = get_candidates(testdb_cursor, source_text_id)
    assert candidates is not None
    assert len(candidates) == POPULATION_SIZE
