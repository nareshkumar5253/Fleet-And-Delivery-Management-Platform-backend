from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.roles import require_admin

from app.schemas.vehicle import (
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse
)
from sqlalchemy.orm import relationship

from app.services.vehicle_service import (
    create_vehicle,
    get_all_vehicles,
    get_vehicle_by_id,
    update_vehicle,
    deactivate_vehicle
)

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)


@router.post(
    "",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):

    new_vehicle = create_vehicle(
        db,
        vehicle
    )

    if not new_vehicle:
        raise HTTPException(
            status_code=400,
            detail="Vehicle already exists"
        )

    return new_vehicle


@router.get(
    "",
    response_model=list[VehicleResponse]
)
def get_vehicles(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):

    return get_all_vehicles(db)


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse
)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):

    vehicle = get_vehicle_by_id(
        db,
        vehicle_id
    )

    drivers = relationship(
    "Driver",
    back_populates="vehicle"
)

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return vehicle


@router.put(
    "/{vehicle_id}",
    response_model=VehicleResponse
)
def update_existing_vehicle(
    vehicle_id: int,
    vehicle: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):

    updated_vehicle = update_vehicle(
        db,
        vehicle_id,
        vehicle
    )

    if not updated_vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return updated_vehicle


@router.put(
    "/{vehicle_id}/deactivate",
    response_model=VehicleResponse
)
def deactivate_existing_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):

    vehicle = deactivate_vehicle(
        db,
        vehicle_id
    )

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return vehicle