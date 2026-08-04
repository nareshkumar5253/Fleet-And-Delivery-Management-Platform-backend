from sqlalchemy.orm import Session

from app.models.driver import Driver, DriverStatus
from app.models.vehicle import Vehicle
from app.models.vehicle import Vehicle, VehicleStatus

from app.schemas.driver import (
    DriverCreate,
    DriverUpdate,
    DriverStatus as DriverStatusSchema
)



# --------------------------------
# Create Driver
# --------------------------------

def create_driver(
    db: Session,
    driver: DriverCreate
):

    existing = (
        db.query(Driver)
        .filter(
            (Driver.phone_number == driver.phone_number)
            |
            (Driver.license_number == driver.license_number)
        )
        .first()
    )


    if existing:
        return None



    db_driver = Driver(
        user_id=driver.user_id,
        name=driver.name,
        phone_number=driver.phone_number,
        license_number=driver.license_number
    )


    db.add(db_driver)

    db.commit()

    db.refresh(db_driver)


    return db_driver




# --------------------------------
# Get All Drivers
# --------------------------------

def get_all_drivers(
    db: Session
):

    return (
        db.query(Driver)
        .all()
    )




# --------------------------------
# Get Driver By ID
# --------------------------------

def get_driver_by_id(
    db: Session,
    driver_id: int
):

    return (
        db.query(Driver)
        .filter(
            Driver.id == driver_id
        )
        .first()
    )




# --------------------------------
# Update Driver
# --------------------------------

def update_driver(
    db: Session,
    driver_id: int,
    data: DriverUpdate
):

    driver = get_driver_by_id(
        db,
        driver_id
    )


    if not driver:
        return None



    update_data = data.model_dump(
        exclude_unset=True
    )


    for key, value in update_data.items():

        setattr(
            driver,
            key,
            value
        )


    db.commit()

    db.refresh(driver)


    return driver




# --------------------------------
# Update Driver Availability
# --------------------------------

def update_driver_status(
    db: Session,
    driver_id: int,
    status: DriverStatusSchema
):

    driver = get_driver_by_id(
        db,
        driver_id
    )


    if not driver:
        return None


    driver.status = status


    db.commit()

    db.refresh(driver)


    return driver





# --------------------------------
# Suspend Driver
# --------------------------------

def suspend_driver(
    db: Session,
    driver_id: int
):

    driver = get_driver_by_id(
        db,
        driver_id
    )


    if not driver:
        return None



    driver.is_active = False

    driver.status = DriverStatus.OFFLINE



    db.commit()

    db.refresh(driver)


    return driver





# --------------------------------
# Assign Vehicle To Driver
# --------------------------------

def assign_vehicle(
    db: Session,
    driver_id: int,
    vehicle_id: int
):

    driver = (
        db.query(Driver)
        .filter(
            Driver.id == driver_id
        )
        .first()
    )


    if not driver:
        return None


    vehicle = (
        db.query(Vehicle)
        .filter(
            Vehicle.id == vehicle_id
        )
        .first()
    )


    if not vehicle:
        return None


    driver.vehicle_id = vehicle_id


    db.commit()

    db.refresh(driver)


    return driver