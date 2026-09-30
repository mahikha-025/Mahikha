
from fastapi import APIRouter

import json
from pathlib import Path

import pandas as pd
from fastapi import HTTPException

from app.database import get_dashboard_summary
from app.services.preprocessing import FEATURES, TARGET, load_sensor_dataset


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def get_dashboard():
    return get_dashboard_summary()


@router.get("/analytics")
def get_analytics():
    project_root = Path(__file__).resolve().parents[2]
    data_path = project_root / "data" / "sensor_data.csv"
    metrics_path = project_root / "models" / "model_metrics.json"
    try:
        raw_data = pd.read_csv(data_path)
        dataset = load_sensor_dataset(data_path)
        with metrics_path.open(encoding="utf-8") as metrics_file:
            metrics = json.load(metrics_file)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise HTTPException(status_code=503, detail=f"Analytics unavailable: {error}")

    features = {
        feature: {
            "mean": round(float(dataset[feature].mean()), 2),
            "std": round(float(dataset[feature].std()), 2),
            "min": round(float(dataset[feature].min()), 2),
            "max": round(float(dataset[feature].max()), 2)
        }
        for feature in FEATURES
    }
    correlation = dataset[FEATURES + [TARGET]].corr()[TARGET].drop(TARGET)

    return {
        "success": True,
        "dataset": {
            "records": len(dataset),
            "raw_records": len(raw_data),
            "failures": int(dataset[TARGET].sum()),
            "failure_rate": round(float(dataset[TARGET].mean() * 100), 2),
            "missing_values": int(raw_data[FEATURES + [TARGET]].isna().sum().sum()),
            "duplicate_rows": int(raw_data.duplicated().sum())
        },
        "features": features,
        "failure_correlation": {key: round(float(value), 3) for key, value in correlation.items()},
        "model_metrics": metrics
    }