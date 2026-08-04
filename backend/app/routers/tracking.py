from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.tracking import TrackingHistory
from app.models.delivery import Delivery

from app.schemas.tracking import (
    TrackingCreate,
    TrackingResponse
)


router = APIRouter(
    prefix="/tracking",
    tags=["Tracking"]
)


@router.post(
    "/update",
    response_model=TrackingResponse
)
def update_location(
    data: TrackingCreate,
    db: Session = Depends(get_db)
):

    delivery = (
        db.query(Delivery)
        .filter(
            Delivery.id == data.delivery_id
        )
        .first()
    )

    if not delivery:
        raise HTTPException(
            status_code=404,
            detail="Delivery not found"
        )


    tracking = TrackingHistory(
        delivery_id=data.delivery_id,
        latitude=data.latitude,
        longitude=data.longitude,
        location=data.location,
        speed=data.speed,
        delivery_status=data.delivery_status
    )


    db.add(tracking)

    db.commit()

    db.refresh(tracking)

    return tracking



@router.get(
    "/{delivery_id}",
    response_model=list[TrackingResponse]
)
def get_tracking_history(
    delivery_id: int,
    db: Session = Depends(get_db)
):

    history = (
        db.query(TrackingHistory)
        .filter(
            TrackingHistory.delivery_id == delivery_id
        )
        .order_by(
            TrackingHistory.created_at.asc()
        )
        .all()
    )

    return history