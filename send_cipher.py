#!/usr/bin/env python3

import httpx
from uuid import UUID
from time import sleep

from celery_decipher.decipher.cipher import cipher
from celery_decipher.decipher.models import DecipherStartResponse, DecipherStatusResponse
from celery_decipher.decipher.solver import get_random_cipher_map


PRATCHETT = """
If you trust in yourself ... and believe in your dreams ... and follow your star ... 
you'll still get beaten by people who spent their time working hard and learning things and weren't so lazy.
"""


def send_cipher_text(text: str) -> UUID:
    """
    Send the cipher text to the server.
    """
    url = "http://localhost:8000/decipher/"
    headers = {"Content-Type": "application/json"}
    data = {"text": text}

    with httpx.Client() as client:
        response = client.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("Cipher text sent successfully.")
            response = DecipherStartResponse.model_validate(response.json())
            return response.source_text_id
        else:
            raise Exception(
                f"Failed to send cipher text. Status code: {response.status_code}"
            )


def get_decipher_status(source_text_id: UUID) -> DecipherStatusResponse:
    """
    Get the status of the deciphering process.
    """
    url = f"http://localhost:8000/decipher/{source_text_id}"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return DecipherStatusResponse.model_validate(response.json())
        else:
            raise Exception(
                f"Failed to get decipher status. Status code: {response.status_code}"
            )


def main():
    cipher_map = get_random_cipher_map()
    ciphered = cipher(PRATCHETT, cipher_map)
    source_text_id = send_cipher_text(ciphered)
    status = get_decipher_status(source_text_id)
    deciphered = None
    score = None
    while status.status != "COMPLETED":
        if deciphered != status.deciphered_text or score != status.score:
            print(f"Score: {round(status.score, 3)}. {status.deciphered_text}")
        deciphered = status.deciphered_text
        score = status.score
        status = get_decipher_status(source_text_id)
        sleep(10)
    unmatched = (
        set((k, v) for k, v in status.cipher_map.items() if k in set(PRATCHETT)) -
        set((k, v) for k, v in cipher_map.items() if k in set(PRATCHETT))
    )
    match_percentage = round(1 - len(unmatched) / len(set(PRATCHETT)), 2) * 100.0
    print(f"Final score: {status.score}. Match: {match_percentage}% {status.deciphered_text}")


if __name__ == "__main__":
    main()
