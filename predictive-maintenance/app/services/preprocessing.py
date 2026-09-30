import pandas as pd
from pathlib import Path


FEATURES = [
    "temperature",
    "pressure",
    "vibration",
    "operating_hours",
    "machine_load"
]
TARGET = "machine_failure"


def preprocess_sensor_data(dataframe):
    required_columns = FEATURES + [TARGET]
    missing_columns = sorted(set(required_columns) - set(dataframe.columns))
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing_columns)}")

    cleaned = dataframe[required_columns].copy()
    cleaned = cleaned.apply(pd.to_numeric, errors="coerce").dropna()
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    if cleaned.empty:
        raise ValueError("Dataset contains no complete sensor records.")
    if not cleaned[TARGET].isin((0, 1)).all():
        raise ValueError("machine_failure must contain only 0 or 1.")
    if (cleaned[FEATURES] < 0).any().any():
        raise ValueError("Sensor measurements cannot be negative.")
    if (cleaned["machine_load"] > 100).any():
        raise ValueError("machine_load must be between 0 and 100.")

    return cleaned


def load_sensor_dataset(data_path=None):
    path = Path(data_path) if data_path else Path(__file__).resolve().parents[2] / "data" / "sensor_data.csv"
    return preprocess_sensor_data(pd.read_csv(path))


def validate_sensor_data(sensor_data):
    dataframe = pd.DataFrame([sensor_data], columns=FEATURES)
    if dataframe.isnull().any().any():
        raise ValueError("Sensor data contains missing values.")
    if (dataframe < 0).any().any() or dataframe["machine_load"].iloc[0] > 100:
        raise ValueError("Sensor measurements are outside the supported range.")
    return dataframe