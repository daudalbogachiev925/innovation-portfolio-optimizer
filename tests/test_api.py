def test_health(client):
    assert client.get("/health").json()["status"] == "ok"

def test_create_project(client):
    payload = {
        "code": "P1", "name": "Test", "investment_m": 10,
        "expected_return_m": 50, "probability_success": 0.6,
        "time_to_market_y": 1, "risk_class": "low", "strategic_fit": 0.8,
    }
    r = client.post("/api/projects", json=payload)
    assert r.status_code == 201
    assert r.json()["code"] == "P1"

def test_optimize_empty(client):
    r = client.post("/api/optimize", json={"budget": 100, "max_high_risk_share": 0.3})
    assert r.status_code == 200
    assert "projects" in r.json()
