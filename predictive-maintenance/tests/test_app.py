from fastapi.testclient import TestClient
import pytest

from app import database
from app.main import app


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "API is running"


def test_prediction_is_stored_and_appears_in_dashboard(monkeypatch, tmp_path):
    monkeypatch.setattr(database, "MONGODB_URI", "")
    monkeypatch.setattr(database, "SQLITE_PATH", tmp_path / "test.db")

    with TestClient(app) as client:
        response = client.post("/api/predict", json={
            "temperature": 72,
            "pressure": 5.2,
            "vibration": 4.8,
            "operating_hours": 1400,
            "machine_load": 65
        })

        assert response.status_code == 200
        prediction = response.json()
        assert 0 <= prediction["failure_probability"] <= 100
        assert prediction["model_used"] == "Random Forest"

        dashboard = client.get("/api/dashboard").json()
        readings = client.get("/api/readings").json()

        assert dashboard["total_readings"] == 1
        assert dashboard["latest_prediction"]["failure_probability"] == prediction["failure_probability"]
        assert readings["count"] == 1
        assert readings["readings"][0]["temperature"] == 72


def test_analytics_reports_dataset_and_model_comparison():
    with TestClient(app) as client:
        response = client.get("/api/dashboard/analytics")

    assert response.status_code == 200
    analytics = response.json()
    assert analytics["dataset"]["records"] > 0
    assert analytics["dataset"]["missing_values"] == 0
    assert set(analytics["model_metrics"]) == {"Random Forest", "Logistic Regression"}
    assert set(analytics["failure_correlation"]) == {
        "temperature", "pressure", "vibration", "operating_hours", "machine_load"
    }


def test_csv_batch_prediction_validates_and_stores_each_reading(monkeypatch, tmp_path):
    monkeypatch.setattr(database, "MONGODB_URI", "")
    monkeypatch.setattr(database, "SQLITE_PATH", tmp_path / "batch.db")
    csv_data = (
        "temperature,pressure,vibration,operating_hours,machine_load\n"
        "72,5.2,4.8,1400,65\n"
        "90,7.1,8.3,3000,88\n"
    )

    with TestClient(app) as client:
        response = client.post("/api/predict/batch", content=csv_data, headers={"content-type": "text/csv"})
        readings = client.get("/api/readings").json()

    assert response.status_code == 200
    assert response.json()["count"] == 2
    assert len(response.json()["results"]) == 2
    assert readings["count"] == 2


def test_required_mongodb_connection_failure_does_not_fall_back(monkeypatch):
    class FailingMongoClient:
        class admin:
            @staticmethod
            def command(_command):
                raise RuntimeError("connection failed")

        def close(self):
            pass

    monkeypatch.setattr(database, "MONGODB_URI", "mongodb://example.invalid")
    monkeypatch.setattr(database, "REQUIRE_MONGODB", True)
    monkeypatch.setattr(database, "MongoClient", lambda *args, **kwargs: FailingMongoClient())
    monkeypatch.setattr(database, "_initialize_sqlite", lambda: pytest.fail("SQLite fallback used"))

    with pytest.raises(RuntimeError, match="MongoDB is required"):
        database.connect_to_database()


def test_required_mongodb_needs_connection_uri(monkeypatch):
    monkeypatch.setattr(database, "MONGODB_URI", "")
    monkeypatch.setattr(database, "REQUIRE_MONGODB", True)
    monkeypatch.setattr(database, "_initialize_sqlite", lambda: pytest.fail("SQLite fallback used"))

    with pytest.raises(RuntimeError, match="MONGODB_URI is not configured"):
        database.connect_to_database()
