from fastapi import APIRouter

from app.database import get_recent_predictions


router = APIRouter(
    prefix="/readings",
    tags=["Readings"]
)


@router.get("")
def get_readings():

    readings = get_recent_predictions(20)

    return {
        "success": True,
        "count": len(readings),
        "readings": readings
    }