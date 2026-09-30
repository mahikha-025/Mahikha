from pydantic import BaseModel, Field


class SensorInput(BaseModel):
    temperature: float = Field(..., ge=0)
    pressure: float = Field(..., ge=0)
    vibration: float = Field(..., ge=0)
    operating_hours: float = Field(..., ge=0)
    machine_load: float = Field(..., ge=0, le=100)


class PredictionResponse(BaseModel):
    prediction: int
    failure_probability: float
    status: str
    model_used: str
    sensor_values: SensorInput


class HealthResponse(BaseModel):
    status: str
    database: str