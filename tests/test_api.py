from fastapi.testclient import TestClient
from api.main import app
client=TestClient(app)

def test_health():
    r=client.get("/health")
    assert r.status_code==200 and r.json()["status"]=="ok"

def test_capabilities():
    r=client.get("/v1/capabilities")
    assert r.status_code==200 and "video" in r.json()["modalities"]

def test_analyze_image():
    r=client.post("/v1/analyze",files={"file":("x.jpg",b"data","image/jpeg")})
    assert r.status_code==200
    assert r.json()["label"]=="UNCERTAIN"

def test_reject_unknown():
    r=client.post("/v1/analyze",files={"file":("x.bin",b"data","application/octet-stream")})
    assert r.status_code==415
