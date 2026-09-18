from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_capabilities():
    response = client.get("/v1/capabilities")
    assert response.status_code == 200
    assert "video" in response.json()["modalities"]


def test_analyze_image():
    response = client.post(
        "/v1/analyze", files={"file": ("x.jpg", b"data", "image/jpeg")}
    )
    assert response.status_code == 200
    assert response.json()["label"] == "UNCERTAIN"


def test_reject_unknown():
    response = client.post(
        "/v1/analyze", files={"file": ("x.bin", b"data", "application/octet-stream")}
    )
    assert response.status_code == 415
