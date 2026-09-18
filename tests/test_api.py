from fastapi.testclient import TestClient

from aidetection.limits import MAX_UPLOAD_BYTES
from api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "AiDetection" in response.text


def test_capabilities():
    response = client.get("/v1/capabilities")
    assert response.status_code == 200
    assert "video" in response.json()["modalities"]


def test_analyze_image():
    response = client.post(
        "/v1/analyze", files={"file": ("x.jpg", b"\xff\xd8\xff\xe0data", "image/jpeg")}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["label"] == "UNCERTAIN"
    assert body["ai_probability"] == 0.5
    assert len(body["request_id"]) == 32
    assert len(body["sha256"]) == 64


def test_reject_unknown():
    response = client.post(
        "/v1/analyze", files={"file": ("x.bin", b"data", "application/octet-stream")}
    )
    assert response.status_code == 415


def test_reject_signature_mismatch():
    response = client.post(
        "/v1/analyze",
        files={"file": ("x.jpg", b"RIFF0000WAVEdata", "image/jpeg")},
    )
    assert response.status_code == 415
    assert response.json()["detail"]["request_id"]


def test_reject_oversized_upload():
    payload = b"x" * (MAX_UPLOAD_BYTES + 1)
    response = client.post(
        "/v1/analyze", files={"file": ("x.jpg", payload, "image/jpeg")}
    )
    assert response.status_code == 413
    assert response.json()["detail"]["request_id"]
