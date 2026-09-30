import os
from pathlib import Path

import joblib
import pandas as pd


BASE_DIRECTORY = Path(__file__).resolve().parents[2]
MODEL_DIRECTORY = BASE_DIRECTORY / "models"

FEATURES = [
    "temperature",
    "pressure",
    "vibration",
    "operating_hours",
    "machine_load"
]


random_forest_model = None
logistic_regression_model = None


def load_models():

    global random_forest_model
    global logistic_regression_model

    random_forest_path = os.path.join(
        MODEL_DIRECTORY,
        "random_forest.pkl"
    )

    logistic_regression_path = os.path.join(
        MODEL_DIRECTORY,
        "logistic_regression.pkl"
    )

    if not os.path.exists(random_forest_path):
        raise FileNotFoundError(
            "Random Forest model not found. "
            "Run ml/train_models.py first."
        )

    if not os.path.exists(logistic_regression_path):
        raise FileNotFoundError(
            "Logistic Regression model not found. "
            "Run ml/train_models.py first."
        )

    random_forest_model = joblib.load(
        random_forest_path
    )

    logistic_regression_model = joblib.load(
        logistic_regression_path
    )


def predict_machine(sensor_values):
    return predict_machines([sensor_values])[0]


def predict_machines(sensor_rows):

    if random_forest_model is None:
        load_models()

    input_data = pd.DataFrame(
        sensor_rows,
        columns=FEATURES
    )

    random_forest_probabilities = random_forest_model.predict_proba(input_data)[:, 1]
    logistic_probabilities = logistic_regression_model.predict_proba(input_data)[:, 1]
    predictions = random_forest_model.predict(input_data)

    results = []
    for prediction, failure_probability, comparison_probability in zip(
        predictions,
        random_forest_probabilities,
        logistic_probabilities
    ):
        if failure_probability < 0.40:
            status = "Normal"
        elif failure_probability < 0.70:
            status = "Maintenance Required"
        else:
            status = "Failure Risk"

        results.append({
            "prediction": int(prediction),
            "failure_probability": round(float(failure_probability) * 100, 2),
            "status": status,
            "model_used": "Random Forest",
            "comparison_probability": round(float(comparison_probability) * 100, 2)
        })

    return results