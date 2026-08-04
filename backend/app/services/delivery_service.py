from sqlalchemy.orm import Session

from app.models.delivery import Delivery, DeliveryStatus
from app.models.driver import Driver, DriverStatus
from app.models.delivery_history import DeliveryStatusHistory
from app.services.notification_service import create_notification

from app.schemas.delivery import (
    DeliveryCreate,
    DeliveryUpdate
)


def create_delivery(
    db: Session,
    delivery: DeliveryCreate
):

    existing_delivery = (
        db.query(Delivery)
        .filter(
            Delivery.tracking_number == delivery.tracking_number
        )
        .first()
    )

    if existing_delivery:
        return None


    new_delivery = Delivery(
        tracking_number=delivery.tracking_number,
        customer_name=delivery.customer_name,
        pickup_address=delivery.pickup_address,
        delivery_address=delivery.delivery_address,
        package_weight=delivery.package_weight,
        priority=delivery.priority,
        scheduled_time=delivery.scheduled_time
    )


    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)

    return new_delivery



def get_all_deliveries(
    db: Session
):

    return db.query(Delivery).all()



def get_delivery_by_id(
    db: Session,
    delivery_id: int
):

    return (
        db.query(Delivery)
        .filter(
            Delivery.id == delivery_id
        )
        .first()
    )



def update_delivery(
    db: Session,
    delivery_id: int,
    delivery: DeliveryUpdate
):

    db_delivery = get_delivery_by_id(
        db,
        delivery_id
    )


    if not db_delivery:
        return None


    update_data = delivery.model_dump(
        exclude_unset=True
    )


    # STATUS HISTORY + NOTIFICATIONS
    if "status" in update_data:

        old_status = db_delivery.status.value
        new_status = update_data["status"].value


        if old_status != new_status:

            history = DeliveryStatusHistory(
                delivery_id=db_delivery.id,
                old_status=old_status,
                new_status=new_status
            )

            db.add(history)



            # DRIVER NOTIFICATION
            if db_delivery.driver_id:

                driver = (
                    db.query(Driver)
                    .filter(
                        Driver.id == db_delivery.driver_id
                    )
                    .first()
                )


                if driver:


                    if new_status == "IN_TRANSIT":

                        create_notification(
                            db,
                            driver.user_id,
                            "Driver started trip."
                        )


                    elif new_status == "DELIVERED":

                        create_notification(
                            db,
                            driver.user_id,
                            "Delivery completed."
                        )


                    elif new_status == "CANCELLED":

                        create_notification(
                            db,
                            driver.user_id,
                            "Delivery cancelled."
                        )


                    elif new_status == "DELAYED":

                        create_notification(
                            db,
                            driver.user_id,
                            "Delivery is delayed."
                        )



    # UPDATE DELIVERY
    for key, value in update_data.items():

        setattr(
            db_delivery,
            key,
            value
        )


    db.commit()
    db.refresh(db_delivery)

    return db_delivery




def assign_delivery(
    db: Session,
    delivery_id: int,
    driver_id: int
):

    delivery = (
        db.query(Delivery)
        .filter(
            Delivery.id == delivery_id
        )
        .first()
    )


    if not delivery:
        return None, "Delivery not found"



    driver = (
        db.query(Driver)
        .filter(
            Driver.id == driver_id
        )
        .first()
    )


    if not driver:
        return None, "Driver not found"



    if not driver.is_active:
        return None, "Driver is suspended"



    if driver.status == DriverStatus.BUSY:
        return None, "Driver is already busy"



    old_status = delivery.status.value


    delivery.driver_id = driver.id

    delivery.status = DeliveryStatus.ASSIGNED


    driver.status = DriverStatus.BUSY



    history = DeliveryStatusHistory(
        delivery_id=delivery.id,
        old_status=old_status,
        new_status="ASSIGNED"
    )

    db.add(history)



    # ASSIGNMENT NOTIFICATION
    create_notification(
        db,
        driver.user_id,
        "You have been assigned a new delivery."
    )



    db.commit()
    db.refresh(delivery)

    return delivery, None




def cancel_delivery(
    db: Session,
    delivery_id: int
):

    delivery = get_delivery_by_id(
        db,
        delivery_id
    )


    if not delivery:
        return None



    old_status = delivery.status.value


    delivery.status = DeliveryStatus.CANCELLED



    history = DeliveryStatusHistory(
        delivery_id=delivery.id,
        old_status=old_status,
        new_status="CANCELLED"
    )

    db.add(history)



    if delivery.driver_id:

        driver = (
            db.query(Driver)
            .filter(
                Driver.id == delivery.driver_id
            )
            .first()
        )


        if driver:

            driver.status = DriverStatus.AVAILABLE


            create_notification(
                db,
                driver.user_id,
                "Delivery cancelled."
            )



    db.commit()
    db.refresh(delivery)

    return delivery




def get_delivery_history(
    db: Session
):

    return (
        db.query(Delivery)
        .order_by(
            Delivery.created_at.desc()
        )
        .all()
    )

from datetime import datetime


def search_deliveries(
    db: Session,
    tracking_number=None,
    driver_id=None,
    vehicle_id=None,
    status=None,
    priority=None,
    start_date=None,
    end_date=None
):

    query = db.query(Delivery)


    if tracking_number:
        query = query.filter(
            Delivery.tracking_number.ilike(
                f"%{tracking_number}%"
            )
        )


    if driver_id:
        query = query.filter(
            Delivery.driver_id == driver_id
        )


    if status:
        query = query.filter(
            Delivery.status == status
        )


    if priority:
        query = query.filter(
            Delivery.priority == priority
        )


    if start_date:
        query = query.filter(
            Delivery.created_at >= start_date
        )


    if end_date:
        query = query.filter(
            Delivery.created_at <= end_date
        )


    return query.all()