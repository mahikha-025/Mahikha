import json
import os
import sys
from pathlib import Path

import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.preprocessing import FEATURES, TARGET, load_sensor_dataset


DATA_PATH = PROJECT_ROOT / "data" / "sensor_data.csv"
MODEL_PATH = PROJECT_ROOT / "models"


def train_models():
    df = load_sensor_dataset(DATA_PATH)

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    random_forest = RandomForestClassifier(
        n_estimators=150,
        random_state=42,
        class_weight="balanced"
    )

    logistic_regression = Pipeline([
        ("scaler", StandardScaler()),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                random_state=42
            )
        )
    ])

    random_forest.fit(X_train, y_train)
    logistic_regression.fit(X_train, y_train)

    models = {
        "Random Forest": random_forest,
        "Logistic Regression": logistic_regression
    }

    metrics = {}

    for model_name, model in models.items():

        predictions = model.predict(X_test)

        metrics[model_name] = {
            "accuracy": round(
                accuracy_score(y_test, predictions), 4
            ),
            "precision": round(
                precision_score(
                    y_test,
                    predictions,
                    zero_division=0
                ),
                4
            ),
            "recall": round(
                recall_score(
                    y_test,
                    predictions,
                    zero_division=0
                ),
                4
            ),
            "f1_score": round(
                f1_score(
                    y_test,
                    predictions,
                    zero_division=0
                ),
                4
            )
        }

    os.makedirs(MODEL_PATH, exist_ok=True)

    joblib.dump(
        random_forest,
        f"{MODEL_PATH}/random_forest.pkl"
    )

    joblib.dump(
        logistic_regression,
        f"{MODEL_PATH}/logistic_regression.pkl"
    )

    with open(
        f"{MODEL_PATH}/model_metrics.json",
        "w"
    ) as file:
        json.dump(metrics, file, indent=4)

    print("\nModel Training Completed.")

    print("\nModel Comparison:")

    for model_name, model_metrics in metrics.items():
        print(f"\n{model_name}")
        print(f"Accuracy : {model_metrics['accuracy']}")
        print(f"Precision: {model_metrics['precision']}")
        print(f"Recall   : {model_metrics['recall']}")
        print(f"F1 Score : {model_metrics['f1_score']}")

    print("\nModels saved successfully.")


if __name__ == "__main__":
    train_models()