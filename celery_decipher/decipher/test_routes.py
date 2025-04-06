from uuid import UUID

from celery_decipher.decipher.models import DecipherStatusResponse


def test_ingest(http_client):
    text = "Smoky smoke test"
    response = http_client.post("/decipher", json={"text": text})
    assert response.status_code == 200
    source_text_id = UUID(response.json()["source_text_id"])

    status_response = http_client.get(f"/decipher/{source_text_id}")
    assert status_response.status_code == 200
    status = DecipherStatusResponse.model_validate(status_response.json())
    assert status.source_text_id == source_text_id
    assert status.source_text == text
    assert status.status == "PENDING"
