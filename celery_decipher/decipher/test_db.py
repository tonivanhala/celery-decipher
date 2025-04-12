from celery_decipher.decipher.db import get_source_text, insert_source_text


def test_insert(testdb_cursor):
    text = "Smoky smoke test"
    source_text_id = insert_source_text(testdb_cursor, text)
    assert source_text_id is not None
    retrieved_text = get_source_text(testdb_cursor, source_text_id)
    assert retrieved_text == text
