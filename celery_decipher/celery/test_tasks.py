from celery_decipher.celery.tasks import initial_guess
from celery_decipher.decipher.db import get_candidates, insert_source_text


def test_initial_guess(testdb_cursor, celery_session_worker):
    text = "Smoky smoke test"
    source_text_id = insert_source_text(testdb_cursor, text)
    testdb_cursor.connection.commit()
    initial_guess.s().delay(source_text_id).get()
    candidates = get_candidates(testdb_cursor, source_text_id)
    assert len(candidates) == 1000
