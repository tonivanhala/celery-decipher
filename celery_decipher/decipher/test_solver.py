from celery_decipher.decipher.cipher import (
    CAESAR_CIPHER,
    ROT13_CIPHER,
    is_valid_cipher_map,
)
from celery_decipher.decipher.db import (
    get_candidates,
    insert_source_text,
)
from celery_decipher.decipher.fixtures import (
    CHURCHILL,
    CHURCHILL_ROT13,
    MANNERHEIM,
)
from celery_decipher.decipher.solver import (
    POPULATION_SIZE,
    crossover,
    fitness,
    initial_guess,
    initial_guess_letter_frequencies,
    mutate,
    word_fitness,
)


def test_fitness():
    score = fitness(CHURCHILL)
    assert score > 0.90
    score = fitness(MANNERHEIM)
    assert score < 0.01


def test_word_fitness():
    score = word_fitness("Action against success.")
    assert score > 0.99
    score = word_fitness(MANNERHEIM)
    assert score < 0.51


def test_crossover():
    result = crossover(CAESAR_CIPHER, ROT13_CIPHER)
    assert is_valid_cipher_map(result)
    assert result != CAESAR_CIPHER
    assert result != ROT13_CIPHER


def test_mutate():
    result = mutate(ROT13_CIPHER)
    assert is_valid_cipher_map(result)


def test_initial_guess_letter_frequencies():
    cipher_map = initial_guess_letter_frequencies(CHURCHILL_ROT13)
    assert is_valid_cipher_map(cipher_map)


def test_initial_guess(testdb_cursor):
    text = "Smoky smoke test"
    source_text_id = insert_source_text(testdb_cursor, text)
    initial_guess(testdb_cursor, source_text_id)
    candidates = get_candidates(testdb_cursor, source_text_id)
    assert candidates is not None
    assert len(candidates) == POPULATION_SIZE
