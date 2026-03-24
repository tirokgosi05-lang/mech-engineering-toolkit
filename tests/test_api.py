from backend.app import app


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_stress_success():
    client = app.test_client()
    response = client.post("/api/stress", json={"force": 1000, "area": 2})
    assert response.status_code == 200
    assert response.get_json()["result"] == 500.0


def test_missing_field_validation():
    client = app.test_client()
    response = client.post("/api/strain", json={"delta_length": 0.1})
    assert response.status_code == 400
    assert "Missing required field" in response.get_json()["error"]


def test_unknown_operation():
    client = app.test_client()
    response = client.post("/api/not_real", json={"x": 1})
    assert response.status_code == 404


def test_api_metadata_contains_operations():
    client = app.test_client()
    response = client.get("/api")
    assert response.status_code == 200
    payload = response.get_json()
    assert "operations" in payload
    assert "stress" in payload["operations"]
