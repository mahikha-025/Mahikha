from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

from app.database import connect_to_database
from app.routes import prediction, readings, dashboard


app = FastAPI(
    title="Predictive Maintenance System",
    description="AI-based machine failure prediction system",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    connect_to_database()


app.include_router(
    prediction.router,
    prefix="/api"
)

app.include_router(
    readings.router,
    prefix="/api"
)

app.include_router(
    dashboard.router,
    prefix="/api"
)


@app.get("/api/health")
def health_check():
    return {
        "status": "API is running"
    }


@app.get("/")
def serve_frontend():
    frontend_path = Path(__file__).resolve().parent.parent / "frontend" / "index.html"

    if frontend_path.exists():
        return FileResponse(str(frontend_path))

    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>Predictive Maintenance</title>
    </head>
    <body>
        <h1>Predictive Maintenance System</h1>
        <p>The API is running and ready to receive sensor payloads.</p>
        <p>Use the backend endpoints under /api to interact with the system.</p>
    </body>
    </html>
    """)