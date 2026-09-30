import os
import json
import sqlite3
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "predictive_maintenance")
REQUIRE_MONGODB = os.getenv("REQUIRE_MONGODB", "").lower() in {"1", "true", "yes"}
SQLITE_PATH = Path(__file__).resolve().parents[1] / "data" / "maintenance.db"

client = None
db = None
database_backend = "sqlite"

sensor_readings_collection = None
predictions_collection = None
model_metrics_collection = None


def connect_to_database():
    global client
    global db
    global database_backend
    global sensor_readings_collection
    global predictions_collection
    global model_metrics_collection

    client = None
    db = None
    sensor_readings_collection = None
    predictions_collection = None
    model_metrics_collection = None

    if MONGODB_URI:
        try:
            client = MongoClient(
                MONGODB_URI,
                serverSelectionTimeoutMS=3000
            )
            client.admin.command("ping")
            db = client[DATABASE_NAME]
            sensor_readings_collection = db["sensor_readings"]
            predictions_collection = db["predictions"]
            model_metrics_collection = db["model_metrics"]
            database_backend = "mongodb"
            return True
        except (PyMongoError, Exception) as error:
            print(f"MongoDB unavailable; using local SQLite storage: {error}")
            if client is not None:
                client.close()
            client = None
            if REQUIRE_MONGODB:
                raise RuntimeError("MongoDB is required but the connection failed.") from error

    if REQUIRE_MONGODB and not MONGODB_URI:
        raise RuntimeError("MongoDB is required but MONGODB_URI is not configured.")

    _initialize_sqlite()
    database_backend = "sqlite"
    return True


def _connect_sqlite():
    SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(SQLITE_PATH, timeout=5)


def _initialize_sqlite():
    with _connect_sqlite() as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS sensor_readings "
            "(id INTEGER PRIMARY KEY, timestamp TEXT NOT NULL, payload TEXT NOT NULL)"
        )
        connection.execute(
            "CREATE TABLE IF NOT EXISTS predictions "
            "(id INTEGER PRIMARY KEY, timestamp TEXT NOT NULL, status TEXT NOT NULL, payload TEXT NOT NULL)"
        )


def get_database():
    if db is None and database_backend != "sqlite":
        connect_to_database()

    return db


def get_sensor_readings_collection():
    if database_backend == "sqlite":
        _initialize_sqlite()
    elif sensor_readings_collection is None:
        connect_to_database()

    return sensor_readings_collection


def get_predictions_collection():
    if database_backend == "sqlite":
        _initialize_sqlite()
    elif predictions_collection is None:
        connect_to_database()

    return predictions_collection


def get_model_metrics_collection():
    if database_backend == "sqlite":
        _initialize_sqlite()
    elif model_metrics_collection is None:
        connect_to_database()

    return model_metrics_collection


def check_database_connection():
    try:
        if database_backend == "mongodb":
            client.admin.command("ping")
        else:
            with _connect_sqlite() as connection:
                connection.execute("SELECT 1")
        return True
    except Exception:
        return False


def _insert_document(table, document):
    timestamp = document["timestamp"].isoformat()
    payload = json.dumps(document, default=lambda value: value.isoformat())
    with _connect_sqlite() as connection:
        if table == "predictions":
            connection.execute(
                "INSERT INTO predictions (timestamp, status, payload) VALUES (?, ?, ?)",
                (timestamp, document["status"], payload)
            )
        else:
            connection.execute(
                "INSERT INTO sensor_readings (timestamp, payload) VALUES (?, ?)",
                (timestamp, payload)
            )


def save_sensor_reading(document):
    collection = get_sensor_readings_collection()
    if database_backend == "mongodb":
        collection.insert_one(document)
    else:
        _insert_document("sensor_readings", document)


def save_prediction(document):
    collection = get_predictions_collection()
    if database_backend == "mongodb":
        collection.insert_one(document)
    else:
        _insert_document("predictions", document)


def get_recent_predictions(limit=20):
    collection = get_predictions_collection()
    if database_backend == "mongodb":
        return list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit))

    with _connect_sqlite() as connection:
        rows = connection.execute(
            "SELECT payload FROM predictions ORDER BY timestamp DESC, id DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [json.loads(row[0]) for row in rows]


def get_dashboard_summary():
    collection = get_predictions_collection()
    if database_backend == "mongodb":
        total = collection.count_documents({})
        statuses = {
            status: collection.count_documents({"status": status})
            for status in ("Normal", "Maintenance Required", "Failure Risk")
        }
        latest = collection.find_one({}, {"_id": 0}, sort=[("timestamp", -1)])
    else:
        with _connect_sqlite() as connection:
            total = connection.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
            statuses = {
                status: count for status, count in connection.execute(
                    "SELECT status, COUNT(*) FROM predictions GROUP BY status"
                ).fetchall()
            }
            latest_row = connection.execute(
                "SELECT payload FROM predictions ORDER BY timestamp DESC, id DESC LIMIT 1"
            ).fetchone()
        latest = json.loads(latest_row[0]) if latest_row else None

    return {
        "success": True,
        "total_readings": total,
        "normal": statuses.get("Normal", 0),
        "maintenance_required": statuses.get("Maintenance Required", 0),
        "failure_risk": statuses.get("Failure Risk", 0),
        "latest_prediction": latest,
        "database": database_backend
    }