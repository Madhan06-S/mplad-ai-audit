import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add backend/ to python path
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "online"

def test_get_projects_endpoint():
    response = client.get("/api/v1/projects?page=1&page_size=5")
    assert response.status_code == 200
    json_data = response.json()
    assert "total_records" in json_data
    assert "data" in json_data
    assert len(json_data["data"]) <= 5

def test_get_analytics_overview_endpoint():
    response = client.get("/api/v1/analytics/overview")
    assert response.status_code == 200
    json_data = response.json()
    assert "total_works" in json_data
    assert "anomalies_count" in json_data
    assert "risk_level_counts" in json_data

def test_pdf_report_endpoint():
    response = client.get("/api/v1/reports/pdf?risk_level=High")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
