# Predictive Maintenance System

A predictive maintenance web application built to monitor industrial machine health using sensor readings and machine learning. The system predicts whether a machine is in a healthy state or at risk of failure using a trained classification model and displays the results in a dashboard.

## Project Objective

This project is designed to help monitor machine condition in real time by analyzing sensor values such as:

- temperature
- pressure
- vibration
- operating hours
- machine load

The application:

- reads incoming sensor data
- preprocesses it for model use
- predicts the machine condition
- stores readings and predictions
- shows recent trends in a dashboard
- compares model performance for analysis

---

## Problem Solved

Modern machines generate large volumes of sensor data. Without predictive monitoring, failures may go unnoticed until serious downtime or damage occurs. This project helps detect abnormal behavior early and supports preventive maintenance decisions.

---

## Tech Stack

- Python
- FastAPI
- Scikit-learn
- Pandas
- NumPy
- SQLite (default storage)
- MongoDB Atlas (optional backup/production storage)
- HTML/CSS/JavaScript frontend

---

## Project Structure

```text
predictive-maintenance/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   └── routes/
│       ├── dashboard.py
│       ├── prediction.py
│       └── readings.py
├── ml/
│   ├── generate_dataset.py
│   └── train_models.py
├── data/
│   ├── sensor_data.csv
│   └── maintenance.db
├── models/
│   └── model_metrics.json
├── frontend/
│   └── index.html
├── tests/
│   └── test_app.py
├── .env
├── requirements.txt
├── run.ps1
├── render.yaml
└── README.md
```

---

## Application Flow

### 1. Data Generation and Model Training

The workflow begins in the machine learning folder:

- `ml/generate_dataset.py` creates synthetic sensor data.
- `ml/train_models.py` trains the classification models.
- Model results and metrics are stored in the `models/` folder.

This creates the baseline model that later predicts machine health.

### 2. API Input

The API receives sensor values through endpoints such as:

- `POST /api/predict`
- `POST /api/predict/batch`

The input data is validated using request schemas and converted into the format expected by the trained model.

### 3. Prediction Process

The system:

- loads the saved model
- preprocesses the incoming values
- predicts failure probability
- assigns a health status such as Normal, Maintenance Required, or Failure Risk

### 4. Storage

Predictions and sensor readings are saved either in:

- SQLite (default local option), or
- MongoDB Atlas (if configured)

The app automatically falls back to SQLite if MongoDB is unavailable or not configured.

### 5. Dashboard

The frontend dashboard shows:

- recent prediction history
- current health summary
- total records
- latest prediction
- analytics and model comparison data

---

## Working of the App

### Start-up behavior

When the app starts:

1. It loads environment variables from `.env`.
2. It checks whether `MONGODB_URI` is available.
3. If MongoDB is reachable, it uses MongoDB.
4. If MongoDB is unavailable, it automatically uses SQLite.
5. The backend continues running and serves the dashboard and APIs.

### Prediction logic

The system evaluates input features and computes whether the machine is likely to fail. A result may include:

- probability score
- prediction status
- selected model name
- timestamp

### Data persistence

Stored data includes:

- sensor readings
- predictions
- model metrics

This allows the dashboard to show historical trends and all recent analysis results.

---

## Database Behavior

### Local mode

The default configuration uses SQLite, which is stored in:

```text
data/maintenance.db
```

This is useful for local development and testing.

### MongoDB mode

MongoDB Atlas can be used for cloud or production-style storage by setting:

```env
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=predictive_maintenance
```

If MongoDB is not reachable, the app logs a warning and continues with SQLite.

---

## API Endpoints

### Health

- `GET /api/health` - checks service status

### Prediction

- `POST /api/predict` - predicts a single reading
- `POST /api/predict/batch` - predicts multiple readings in CSV format

### Readings

- `GET /api/readings` - returns recent readings and predictions

### Dashboard

- `GET /api/dashboard` - summary of latest prediction and counts
- `GET /api/dashboard/analytics` - model comparison and analytics data

### Frontend

- `GET /` - main dashboard page

---

## Run Locally

From the project folder, create a virtual environment and install dependencies:

```powershell
cd D:\MAHII\Mahikha\predictive-maintenance
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python ml/generate_dataset.py
python ml/train_models.py
```

Then start the app:

```powershell
.\run.ps1
```

Or directly:

```powershell
uvicorn app.main:app --reload
```

Open the app in the browser:

```text
http://127.0.0.1:8000
```

The API docs are available at:

```text
http://127.0.0.1:8000/docs
```

---

## Environment Variables

Create a `.env` file in the project root with values similar to:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=Cluster0
DATABASE_NAME=predictive_maintenance
REQUIRE_MONGODB=false
```

If MongoDB is not needed for local testing, keep it unset or set `REQUIRE_MONGODB=false`.

---

## Deployment

This project also includes a Render deployment setup in `render.yaml`.

For deployment:

- configure a MongoDB Atlas database
- provide `MONGODB_URI` as a secret in Render
- ensure network access is enabled for the service
- keep credentials out of Git

The app is designed to fail cleanly and clearly if MongoDB is required but unreachable.

---

## Data and Model Notes

- The dataset is synthetic demonstration data for training and testing.
- `generate_dataset.py` creates a fixed dataset for reproducible results.
- `train_models.py` trains multiple models and evaluates them.
- Metrics are stored in `models/model_metrics.json`.

This project is meant for demonstration and learning, but the architecture can be extended to real machine sensor datasets and production deployment environments.

---

## Testing

Run the test suite with:

```powershell
python -m pytest
```

---

## Summary

This project demonstrates a complete predictive maintenance pipeline:

- data generation
- preprocessing
- model training
- prediction API
- database storage
- dashboard visualization
- deployment-ready architecture

It is a practical example of how machine learning can be integrated into a monitoring application for industrial maintenance planning.
