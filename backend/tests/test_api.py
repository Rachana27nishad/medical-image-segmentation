from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "version" in r.json()


def test_models_list_marks_status():
    r = client.get("/api/v1/models")
    assert r.status_code == 200
    status = {m["id"]: m["status"] for m in r.json()["models"]}
    assert status["unet"] == "implemented"
    assert status["attention_unet"] == "planned"


def test_samples():
    r = client.get("/api/v1/data/samples")
    assert r.status_code == 200
    assert len(r.json()["samples"]) == 3


def test_preprocess_sample_with_window_and_clahe():
    r = client.post(
        "/api/v1/preprocess",
        data={"sample_id": "lung_ct", "window_preset": "lung", "apply_clahe": "true"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["original_b64"].startswith("data:image/png;base64,")
    assert body["processed_b64"].startswith("data:image/png;base64,")
    assert body["stats"]["processed"]["max"] > body["stats"]["processed"]["min"]


def test_preprocess_unknown_sample():
    r = client.post("/api/v1/preprocess", data={"sample_id": "nope"})
    assert r.status_code == 404


def test_planned_endpoints_return_501():
    assert client.post("/api/v1/segment").status_code == 501
    assert client.post("/api/v1/evaluate/benchmark").status_code == 501
