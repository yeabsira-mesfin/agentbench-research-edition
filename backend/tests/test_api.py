from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def payload(**changes):
    return {"task_id": "AUTH-101", "satisfied_checks": [f"c{i}" for i in range(5)], "explanation": "Review evidence: atomic rotation and concurrent regression test plan.", "maintainability": True, "documentation": True, **changes}

def test_task_registry_has_unique_ids_and_public_criteria():
    tasks = client.get("/api/tasks").json()
    assert len(tasks) == 6 and len({t["id"] for t in tasks}) == 6
    assert all(len(t["checks"]) == 5 for t in tasks)

def test_full_attestation_is_explicitly_not_execution():
    r = client.post("/api/evaluate", json=payload()).json()
    assert r["score"] == 100 and r["release_ready"]
    assert r["mode"] == "reviewer_attested" and r["executed_tests"] == 0

def test_security_gate_fails_even_with_high_numeric_score():
    r = client.post("/api/evaluate", json=payload(satisfied_checks=["c0", "c1", "c3", "c4"])).json()
    assert r["score"] == 80 and not r["release_ready"]

def test_regression_gate_and_partial_credit():
    r = client.post("/api/evaluate", json=payload(satisfied_checks=["c0", "c1", "c2", "c3"])).json()
    assert r["score"] == 92.5 and not r["gates"]["regression_safety"]

def test_unknown_task_and_duplicate_checks():
    assert client.post("/api/evaluate", json=payload(task_id="unknown")).status_code == 404
    assert client.post("/api/evaluate", json=payload(satisfied_checks=["c0", "c0"])).status_code == 422

def test_invalid_and_oversized_input():
    for changes in [{"explanation": "short"}, {"explanation": "x" * 4001}, {"satisfied_checks": ["unknown"]}]:
        assert client.post("/api/evaluate", json=payload(**changes)).status_code == 422
    assert client.post("/evaluate", json={"correctness": -1}).status_code == 422

