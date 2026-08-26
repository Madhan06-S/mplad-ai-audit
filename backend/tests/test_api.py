import os
import sys
import pytest
from fastapi.testclient import TestClient

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "backend", "app"))

from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "html" in response.headers.get("content-type", "").lower()

def test_get_kpis():
    response = client.get("/api/kpis")
    assert response.status_code == 200
    data = response.json()
    assert data["total_works"] == 33000
    assert data["critical_risk_count"] >= 0

def test_get_projects_list():
    response = client.get("/api/projects?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    assert "composite_risk_score" in data[0]
    assert data[0]["data_source"] == "real_esakshi"

def test_get_investigation_queue():
    response = client.get("/api/projects/queue?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["risk_level"] in ["Critical", "High"]

def test_explain_project():
    response_q = client.get("/api/projects/queue?limit=1")
    work_id = response_q.json()[0]["work_id"]
    
    response_exp = client.get("/api/projects/explain", params={"work_id": work_id})
    assert response_exp.status_code == 200
    exp = response_exp.json()
    assert "explainability_reasons" in exp
    assert "disclaimer" in exp
    assert "evidence" in exp
