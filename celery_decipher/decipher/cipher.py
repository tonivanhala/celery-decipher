from typing import TypeAlias, TypeGuard
from uuid import UUID

SingleLowercaseChar: TypeAlias = str
CandidateID: TypeAlias = UUID
CipherMap: TypeAlias = dict[SingleLowercaseChar, SingleLowercaseChar]

ALL_LETTERS = {chr(ch) for ch in range(ord("a"), ord("z") + 1)}
CAESAR_CIPHER = {
    k: v
    for k, v in zip(
        "abcdefghijklmnopqrstuvwxyz",
        "defghijklmnopqrstuvwxyzabc",
    )
}
ROT13_CIPHER = {
    k: v
    for k, v in zip(
        "abcdefghijklmnopqrstuvwxyz",
        "nopqrstuvwxyzabcdefghijklm",
    )
}


def is_single_char(s: str) -> TypeGuard[SingleLowercaseChar]:
    """Check if a string is a single character."""
    return len(s) == 1


def is_single_lowercase_char(s: str) -> TypeGuard[SingleLowercaseChar]:
    """Check if a string is a single lowercase character."""
    return is_single_char(s) and s.islower()


def is_cipher_map(m: dict[str, str]) -> TypeGuard[CipherMap]:
    """Check if a dictionary is a valid cipher map."""
    return all(
        is_single_lowercase_char(k)
        and is_single_lowercase_char(v)
        and k in ALL_LETTERS
        and v in ALL_LETTERS
        for k, v in m.items()
    )


def is_valid_cipher_map(m: dict[str, str]) -> bool:
    """Check if a dictionary contains all letters from a to z and maps them uniquely to other letters."""
    keys = {k for k in m.keys() if is_single_lowercase_char(k)}
    values = {k for k in m.values() if is_single_lowercase_char(k)}
    return (
        len(keys) == len(values) == len(ALL_LETTERS)
        and keys == ALL_LETTERS
        and values == ALL_LETTERS
    )


def replace_character(ch: SingleLowercaseChar, cipher_map: CipherMap) -> str:
    """Replace character maintaining case"""
    if ch.islower():
        return cipher_map.get(ch, ch)
    elif ch.isupper():
        lower_ch = ch.lower()
        return cipher_map.get(lower_ch, lower_ch).upper()
    return ch


def cipher(text: str, cipher_map: CipherMap) -> str:
    """Cipher text using a cipher map."""
    return "".join(replace_character(c, cipher_map) for c in text)


def decipher(text: str, cipher_map: CipherMap) -> str:
    """Decipher text using a cipher map."""
    decipher_key = {v: k for k, v in cipher_map.items()}
    return cipher(text, decipher_key)
