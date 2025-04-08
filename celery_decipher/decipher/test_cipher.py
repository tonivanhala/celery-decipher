from celery_decipher.decipher.cipher import (
    ROT13_CIPHER,
    cipher,
    decipher,
    is_valid_cipher_map,
)
from celery_decipher.decipher.fixtures import (
    CHURCHILL,
    CHURCHILL_ROT13,
    ROT13_MISSING_LETTER,
)


def test_is_valid_cipher_map():
    assert is_valid_cipher_map(ROT13_CIPHER)
    assert not is_valid_cipher_map(ROT13_MISSING_LETTER)


def test_decipher():
    text = "cat"
    ciphered = cipher(text, ROT13_CIPHER)
    assert ciphered == "png"
    deciphered = decipher(ciphered, ROT13_CIPHER)
    assert deciphered == "cat"


def test_cipher_punctuation():
    ciphered = cipher(CHURCHILL, ROT13_CIPHER)
    assert ciphered == CHURCHILL_ROT13
    deciphered = decipher(ciphered, ROT13_CIPHER)
    assert deciphered == CHURCHILL
