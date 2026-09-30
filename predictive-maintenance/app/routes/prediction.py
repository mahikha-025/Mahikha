import csv
import io
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request

from app.schemas import SensorInput
from app.database import (
    save_sensor_reading,
    save_prediction
)
from app.services.ml_service import predict_machine, predict_machines


router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)
MAX_CSV_BYTES = 2_000_000
MAX_BATCH_ROWS = 5000


@router.post("")
def predict(sensor_data: SensorInput):

    try:
        sensor_values = sensor_data.model_dump()

        result = predict_machine(
            sensor_values
        )

        timestamp = datetime.now(
            timezone.utc
        )

        sensor_document = {
            **sensor_values,
            "timestamp": timestamp
        }

        prediction_document = {
            **sensor_values,
            "prediction": result["prediction"],
            "failure_probability": result[
                "failure_probability"
            ],
            "status": result["status"],
            "model_used": result["model_used"],
            "timestamp": timestamp
        }

        save_sensor_reading(sensor_document)
        save_prediction(prediction_document)

        return {
            "success": True,
            "prediction": result["prediction"],
            "failure_probability": result[
                "failure_probability"
            ],
            "status": result["status"],
            "model_used": result["model_used"],
            "sensor_values": sensor_values
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.post("/batch")
async def predict_batch(request: Request):
    csv_bytes = await request.body()
    if len(csv_bytes) > MAX_CSV_BYTES:
        raise HTTPException(status_code=413, detail="CSV file must be 2 MB or smaller.")

    try:
        csv_text = csv_bytes.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(csv_text))
        if not reader.fieldnames:
            raise HTTPException(status_code=422, detail="CSV must include a header row.")

        required_fields = set(SensorInput.model_fields)
        missing_fields = sorted(required_fields - set(reader.fieldnames))
        if missing_fields:
            raise HTTPException(
                status_code=422,
                detail=f"CSV is missing required columns: {', '.join(missing_fields)}"
            )

        sensor_rows = []
        source_rows = []
        for row_number, row in enumerate(reader, start=2):
            if not any(value and value.strip() for value in row.values() if value):
                continue
            try:
                sensor_data = SensorInput.model_validate(row).model_dump()
            except Exception as error:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid sensor data on CSV row {row_number}: {error}"
                ) from error
            sensor_rows.append(sensor_data)
            source_rows.append(row_number)
            if len(sensor_rows) > MAX_BATCH_ROWS:
                raise HTTPException(status_code=413, detail="CSV cannot contain more than 5,000 readings.")

        if not sensor_rows:
            raise HTTPException(status_code=422, detail="CSV contains no sensor readings.")
    except UnicodeDecodeError as error:
        raise HTTPException(status_code=422, detail="CSV must use UTF-8 encoding.") from error

    try:
        predictions = predict_machines(sensor_rows)
        timestamp = datetime.now(timezone.utc)
        results = []
        for row_number, sensor_values, result in zip(source_rows, sensor_rows, predictions):
            sensor_document = {**sensor_values, "timestamp": timestamp}
            prediction_document = {
                **sensor_values,
                **result,
                "timestamp": timestamp
            }
            save_sensor_reading(sensor_document)
            save_prediction(prediction_document)
            results.append({"row_number": row_number, **sensor_values, **result})

        status_counts = {
            status: sum(result["status"] == status for result in results)
            for status in ("Normal", "Maintenance Required", "Failure Risk")
        }
        return {
            "success": True,
            "count": len(results),
            "average_failure_probability": round(
                sum(result["failure_probability"] for result in results) / len(results), 2
            ),
            "status_counts": status_counts,
            "results": results
        }
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error