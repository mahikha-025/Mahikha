# Predictive Maintenance System

A machine-monitoring application that estimates failure probability from five sensor measurements, stores readings and predictions, and compares two classification models.

## Run Locally

From the project directory, install dependencies and prepare the dataset and model files:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python ml/generate_dataset.py
python ml/train_models.py
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` for the monitoring dashboard or `http://127.0.0.1:8000/docs` for the API reference. The app uses persistent SQLite storage in `data/maintenance.db` by default. To use MongoDB Atlas instead, set `MONGODB_URI` (and optionally `DATABASE_NAME`) in `.env`; SQLite is used automatically if MongoDB is not configured or cannot be reached.

## Deploy to Render

The repository-root `render.yaml` defines the web service, health check, and build step. Render trains the models during the build because the model artifacts are excluded from Git. Create a MongoDB Atlas database, configure its network access for the Render service, and add `MONGODB_URI` as a secret environment variable in Render. The service sets `REQUIRE_MONGODB=true`, so it will fail to start rather than silently use non-persistent SQLite if Atlas is missing or unreachable. Keep database credentials out of Git and use a least-privilege Atlas database user.

Create a Render Blueprint from the repository and deploy the `predictive-maintenance` project. The local files must be committed and pushed to the connected GitHub branch before Render can build them.

## Data and Models

The included 2,000-row sensor dataset is generated synthetic demonstration data, not readings from a deployed machine. `python ml/generate_dataset.py` recreates it with a fixed random seed. Training preprocessing selects the required sensor and target fields, coerces numeric values, removes incomplete and duplicate records, and validates ranges and binary labels. Replace the CSV with representative, labeled machine data before using the probability estimates operationally.

`python ml/train_models.py` trains a Random Forest and a scaled Logistic Regression classifier using a stratified holdout split. It saves model artifacts and accuracy, precision, recall, and F1 metrics under `models/`. The dashboard's training profile reports dataset quality, sensor statistics, and each feature's correlation with failure; its signal chart and history table use live stored predictions.

## API

- `GET /api/health` reports API availability.
- `POST /api/predict` accepts `temperature`, `pressure`, `vibration`, `operating_hours`, and `machine_load`; returns failure probability, status, and model.
- `POST /api/predict/batch` accepts a UTF-8 CSV request body with those five column headers, scores up to 5,000 rows (2 MB maximum), and stores each reading and prediction.
- `GET /api/readings` returns the 20 most recent saved predictions.
- `GET /api/dashboard` returns reading totals by health status and the latest prediction.
- `GET /api/dashboard/analytics` returns training-data EDA and model comparison metrics.

The dashboard accepts a sensor CSV and provides per-row predictions as a downloadable CSV. The source dataset may also contain the `machine_failure` target column; it is ignored during prediction.

Run tests with `python -m pytest`.
