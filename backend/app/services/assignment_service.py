from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.delivery import Delivery, DeliveryStatus
from app.models.delivery_assignment import DeliveryAssignment


def create_assignment(db: Session, data):

    # Find delivery
    delivery = (
        db.query(Delivery)
        .filter(Delivery.id == data.delivery_id)
        .first()
    )

    if not delivery:
        raise HTTPException(
            status_code=404,
            detail="Delivery not found"
        )

    # Create assignment
    assignment = DeliveryAssignment(
        delivery_id=data.delivery_id,
        driver_id=data.driver_id,
        vehicle_id=data.vehicle_id,
        estimated_distance=data.estimated_distance,
        estimated_time=data.estimated_time
    )

    db.add(assignment)

    # IMPORTANT:
    # Update delivery table also
    delivery.driver_id = data.driver_id
    delivery.status = DeliveryStatus.ASSIGNED

    db.commit()

    db.refresh(assignment)

    return assignment