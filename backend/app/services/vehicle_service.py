from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


def create_vehicle(
    db: Session,
    vehicle: VehicleCreate
):

    existing_vehicle = db.query(Vehicle).filter(
        Vehicle.vehicle_number == vehicle.vehicle_number
    ).first()

    if existing_vehicle:
        return None

    new_vehicle = Vehicle(
        vehicle_number=vehicle.vehicle_number,
        vehicle_type=vehicle.vehicle_type,
        capacity=vehicle.capacity,
        fuel_type=vehicle.fuel_type
    )

    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)

    return new_vehicle


def get_all_vehicles(
    db: Session
):

    return db.query(Vehicle).all()


def get_vehicle_by_id(
    db: Session,
    vehicle_id: int
):

    return db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()


def update_vehicle(
    db: Session,
    vehicle_id: int,
    vehicle: VehicleUpdate
):

    db_vehicle = get_vehicle_by_id(
        db,
        vehicle_id
    )

    if not db_vehicle:
        return None

    update_data = vehicle.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_vehicle,
            key,
            value
        )

    db.commit()
    db.refresh(db_vehicle)

    return db_vehicle


def deactivate_vehicle(
    db: Session,
    vehicle_id: int
):

    db_vehicle = get_vehicle_by_id(
        db,
        vehicle_id
    )

    if not db_vehicle:
        return None

    db_vehicle.is_active = False

    db.commit()
    db.refresh(db_vehicle)

    return db_vehicle