from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.dependencies.roles import require_admin_or_dispatcher, require_delivery_user

from app.schemas.delivery import (
    DeliveryCreate,
    DeliveryUpdate,
    DeliveryResponse
)

from app.schemas.delivery_history import (
    DeliveryStatusHistoryResponse
)

from app.models.delivery_history import DeliveryStatusHistory

from app.services.delivery_service import (
    create_delivery,
    get_all_deliveries,
    get_delivery_by_id,
    update_delivery,
    assign_delivery,
    cancel_delivery,
    get_delivery_history,
    search_deliveries
)


router = APIRouter(
    prefix="/deliveries",
    tags=["Deliveries"]
)


# ------------------------
# Create Delivery
# ------------------------
@router.post(
    "",
    response_model=DeliveryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_delivery(
    delivery: DeliveryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_dispatcher())
):

    new_delivery = create_delivery(
        db,
        delivery
    )

    if not new_delivery:
        raise HTTPException(
            status_code=400,
            detail="Tracking number already exists"
        )

    return new_delivery



# ------------------------
# Get All Deliveries
# ------------------------
@router.get(
    "",
    response_model=list[DeliveryResponse]
)
def get_deliveries(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_dispatcher())
):

    return get_all_deliveries(db)



# ------------------------
# Delivery History
# ------------------------
@router.get(
    "/history",
    response_model=list[DeliveryResponse]
)
def delivery_history(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_dispatcher())
):

    return get_delivery_history(db)



# ------------------------
# Search Deliveries
# KEEP THIS BEFORE /{delivery_id}
# ------------------------
@router.get("/search")
def search_delivery_orders(
    tracking_number: str | None = None,
    driver_id: int | None = None,
    vehicle_id: int | None = None,
    status: str | None = None,
    priority: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,

    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_dispatcher())
):

    return search_deliveries(
        db,
        tracking_number,
        driver_id,
        vehicle_id,
        status,
        priority,
        start_date,
        end_date
    )



# ------------------------
# Delivery Status Timeline
# ------------------------
@router.get(
    "/{delivery_id}/history",
    response_model=list[DeliveryStatusHistoryResponse]
)
def delivery_status_history(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_delivery_user())

):

    history = (
        db.query(DeliveryStatusHistory)
        .filter(
            DeliveryStatusHistory.delivery_id == delivery_id
        )
        .order_by(
            DeliveryStatusHistory.changed_at
        )
        .all()
    )

    return history



# ------------------------
# Get Delivery By ID
# ------------------------
@router.get(
    "/{delivery_id}",
    response_model=DeliveryResponse
)
def get_delivery(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_dispatcher())
):

    delivery = get_delivery_by_id(
        db,
        delivery_id
    )

    if not delivery:
        raise HTTPException(
            status_code=404,
            detail="Delivery not found"
        )

    return delivery



# ------------------------
# Update Delivery
# ------------------------
@router.put(
    "/{delivery_id}",
    response_model=DeliveryResponse
)
def update_existing_delivery(
    delivery_id: int,
    delivery: DeliveryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_delivery_user())
):

    existing_delivery = get_delivery_by_id(
        db,
        delivery_id
    )

    if not existing_delivery:
        raise HTTPException(
            status_code=404,
            detail="Delivery not found"
        )


    # DRIVER can update only assigned deliveries
    if current_user.role.value == "DRIVER":

        if existing_delivery.driver_id != current_user.driver.id:
            raise HTTPException(
                status_code=403,
                detail="You can update only assigned deliveries"
            )


    updated_delivery = update_delivery(
        db,
        delivery_id,
        delivery
    )


    return updated_delivery


# ------------------------
# Assign Driver
# ------------------------
@router.put(
    "/{delivery_id}/assign/{driver_id}",
    response_model=DeliveryResponse
)
def assign_delivery_to_driver(
    delivery_id: int,
    driver_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_dispatcher())
):

    delivery, error = assign_delivery(
        db,
        delivery_id,
        driver_id
    )

    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return delivery



# ------------------------
# Cancel Delivery
# ------------------------
@router.put(
    "/{delivery_id}/cancel",
    response_model=DeliveryResponse
)
def cancel_existing_delivery(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_dispatcher())
):

    delivery = cancel_delivery(
        db,
        delivery_id
    )

    if not delivery:
        raise HTTPException(
            status_code=404,
            detail="Delivery not found"
        )

    return delivery