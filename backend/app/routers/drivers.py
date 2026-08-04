from app.dependencies.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.roles import require_admin
from app.models.delivery import Delivery

from app.schemas.driver import (
    DriverCreate,
    DriverUpdate,
    DriverResponse,
    DriverStatus
)

from app.services.driver_service import (
    create_driver,
    get_all_drivers,
    get_driver_by_id,
    update_driver,
    suspend_driver,
    assign_vehicle,
    update_driver_status
)


router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)


# -----------------------------
# Create Driver
# -----------------------------

@router.post(
    "",
    response_model=DriverResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_driver(
    driver: DriverCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):

    new_driver = create_driver(
        db,
        driver
    )

    if not new_driver:
        raise HTTPException(
            status_code=400,
            detail="Driver already exists"
        )

    return new_driver



# -----------------------------
# Get All Drivers
# -----------------------------

@router.get(
    "",
    response_model=list[DriverResponse]
)
def get_drivers(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):

    return get_all_drivers(db)



# -----------------------------
# Get Driver By ID
# -----------------------------

@router.get(
    "/{driver_id}",
    response_model=DriverResponse
)
def get_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):

    driver = get_driver_by_id(
        db,
        driver_id
    )

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    return driver



# -----------------------------
# Update Driver
# -----------------------------

@router.put(
    "/{driver_id}",
    response_model=DriverResponse
)
def update_existing_driver(
    driver_id: int,
    driver: DriverUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):

    updated_driver = update_driver(
        db,
        driver_id,
        driver
    )

    if not updated_driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    return updated_driver



# -----------------------------
# Update Driver Availability
# -----------------------------

@router.put(
    "/{driver_id}/status",
    response_model=DriverResponse
)
def update_driver_availability(
    driver_id: int,
    status: DriverStatus,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):

    driver = update_driver_status(
        db,
        driver_id,
        status
    )

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    return driver



# -----------------------------
# Suspend Driver
# -----------------------------

@router.put(
    "/{driver_id}/suspend",
    response_model=DriverResponse
)
def suspend_existing_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):

    driver = suspend_driver(
        db,
        driver_id
    )

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    return driver



# -----------------------------
# Assign Vehicle
# -----------------------------

@router.put(
    "/{driver_id}/vehicle/{vehicle_id}",
    response_model=DriverResponse
)
def assign_driver_vehicle(
    driver_id: int,
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):

    driver = assign_vehicle(
        db,
        driver_id,
        vehicle_id
    )


    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver or Vehicle not found"
        )


    return driver

@router.get(
    "/{driver_id}/deliveries"
)
def get_driver_deliveries(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    deliveries = (
        db.query(Delivery)
        .filter(
            Delivery.driver_id == driver_id
        )
        .all()
    )

    return deliveries