from pathlib import Path
import numpy as np
import pandas as pd


RANDOM_SEED = 42
NUMBER_OF_RECORDS = 2000
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sensor_data.csv"


def generate_dataset():
    np.random.seed(RANDOM_SEED)

    temperature = np.random.normal(70, 15, NUMBER_OF_RECORDS)
    pressure = np.random.normal(5, 1.5, NUMBER_OF_RECORDS)
    vibration = np.random.normal(5, 2, NUMBER_OF_RECORDS)
    operating_hours = np.random.uniform(100, 5000, NUMBER_OF_RECORDS)
    machine_load = np.random.uniform(20, 100, NUMBER_OF_RECORDS)

    temperature = np.clip(temperature, 30, 120)
    pressure = np.clip(pressure, 1, 10)
    vibration = np.clip(vibration, 0.5, 15)
    operating_hours = np.clip(operating_hours, 100, 5000)
    machine_load = np.clip(machine_load, 20, 100)

    risk_score = (
        (temperature - 60) / 25
        + (pressure - 4) / 3
        + (vibration - 3) / 4
        + (operating_hours - 1000) / 3000
        + (machine_load - 50) / 50
    )

    probability = 1 / (1 + np.exp(-risk_score))

    machine_failure = (
        np.random.random(NUMBER_OF_RECORDS) < probability
    ).astype(int)

    df = pd.DataFrame({
        "temperature": temperature.round(2),
        "pressure": pressure.round(2),
        "vibration": vibration.round(2),
        "operating_hours": operating_hours.round(2),
        "machine_load": machine_load.round(2),
        "machine_failure": machine_failure
    })

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

    print("Dataset generated successfully.")
    print(f"Dataset shape: {df.shape}")

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nFailure distribution:")
    print(df["machine_failure"].value_counts())

    print(f"\nSaved to: {DATA_PATH}")


if __name__ == "__main__":
    generate_dataset()