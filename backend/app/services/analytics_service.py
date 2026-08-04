from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.driver import Driver, DriverStatus
from app.models.vehicle import Vehicle, VehicleStatus
from app.models.delivery import Delivery, DeliveryStatus
from app.models.delivery_history import DeliveryStatusHistory
import json

from app.core.redis import redis_client

def get_dashboard(db: Session):

    # ----------------------------
    # Check Redis Cache
    # ----------------------------

    cached_dashboard = redis_client.get("analytics_dashboard")

    if cached_dashboard:
        print("Loaded Dashboard From Redis")
        return json.loads(cached_dashboard)

    print("Loaded Dashboard From PostgreSQL")

    # ==========================
    # DRIVER ANALYTICS
    # ==========================

    total_drivers = db.query(Driver).count()

    active_drivers = (
        db.query(Driver)
        .filter(
            Driver.is_active == True
        )
        .count()
    )

    available_drivers = (
        db.query(Driver)
        .filter(
            Driver.status == DriverStatus.AVAILABLE
        )
        .count()
    )

    busy_drivers = (
        db.query(Driver)
        .filter(
            Driver.status == DriverStatus.BUSY
        )
        .count()
    )


    # ==========================
    # VEHICLE ANALYTICS
    # ==========================

    total_vehicles = db.query(Vehicle).count()

    active_vehicles = (
        db.query(Vehicle)
        .filter(
            Vehicle.is_active == True
        )
        .count()
    )

    available_vehicles = (
        db.query(Vehicle)
        .filter(
            Vehicle.status == VehicleStatus.AVAILABLE
        )
        .count()
    )

    vehicles_in_use = (
        db.query(Vehicle)
        .filter(
            Vehicle.status == VehicleStatus.IN_USE
        )
        .count()
    )

    vehicles_in_maintenance = (
        db.query(Vehicle)
        .filter(
            Vehicle.status == VehicleStatus.MAINTENANCE
        )
        .count()
    )


    vehicle_utilization = 0

    if total_vehicles > 0:
        vehicle_utilization = round(
            (vehicles_in_use / total_vehicles) * 100,
            2
        )


    # ==========================
    # DELIVERY ANALYTICS
    # ==========================

    total_deliveries = db.query(Delivery).count()


    pending_deliveries = (
        db.query(Delivery)
        .filter(
            Delivery.status == DeliveryStatus.PENDING
        )
        .count()
    )


    assigned_deliveries = (
        db.query(Delivery)
        .filter(
            Delivery.status == DeliveryStatus.ASSIGNED
        )
        .count()
    )


    in_transit_deliveries = (
        db.query(Delivery)
        .filter(
            Delivery.status == DeliveryStatus.IN_TRANSIT
        )
        .count()
    )


    active_deliveries = (
        db.query(Delivery)
        .filter(
            Delivery.status.in_(
                [
                    DeliveryStatus.ASSIGNED,
                    DeliveryStatus.PICKED_UP,
                    DeliveryStatus.IN_TRANSIT
                ]
            )
        )
        .count()
    )


    delivered_deliveries = (
        db.query(Delivery)
        .filter(
            Delivery.status == DeliveryStatus.DELIVERED
        )
        .count()
    )


    cancelled_deliveries = (
        db.query(Delivery)
        .filter(
            Delivery.status == DeliveryStatus.CANCELLED
        )
        .count()
    )


    # ==========================
    # AVERAGE DELIVERY TIME
    # ==========================

    average_delivery_time = 0

    delivered_history = (
        db.query(DeliveryStatusHistory)
        .filter(
            DeliveryStatusHistory.new_status == "DELIVERED"
        )
        .all()
    )


    if delivered_history:

        total_minutes = 0

        count = 0

        for history in delivered_history:

            delivery = (
                db.query(Delivery)
                .filter(
                    Delivery.id == history.delivery_id
                )
                .first()
            )

            if delivery:

                time_difference = (
                    history.changed_at -
                    delivery.created_at
                )

                total_minutes += (
                    time_difference.total_seconds()
                    / 60
                )

                count += 1


        if count > 0:

            average_delivery_time = round(
                total_minutes / count,
                2
            )


    # ==========================
    # TOP PERFORMING DRIVERS
    # ==========================

    top_drivers = (
        db.query(
            Driver.id.label("driver_id"),
            Driver.name,
            func.count(Delivery.id)
            .label("completed_deliveries")
        )
        .join(
            Delivery,
            Delivery.driver_id == Driver.id
        )
        .filter(
            Delivery.status == DeliveryStatus.DELIVERED
        )
        .group_by(
            Driver.id
        )
        .order_by(
            func.count(Delivery.id).desc()
        )
        .limit(5)
        .all()
    )


    top_performing_drivers = []

    for driver in top_drivers:

        top_performing_drivers.append(
            {
                "driver_id": driver.driver_id,
                "driver_name": driver.name,
                "completed_deliveries":
                    driver.completed_deliveries
            }
        )


    # ==========================
    # SUCCESS RATE
    # ==========================

    delivery_success_rate = 0

    total_completed_attempts = (
        total_deliveries -
        cancelled_deliveries
    )


    if total_completed_attempts > 0:

        delivery_success_rate = round(
            (
                delivered_deliveries /
                total_completed_attempts
            ) * 100,
            2
        )

    # ==========================
    # FINAL RESPONSE
    # ==========================

    dashboard_data = {

        "total_drivers": total_drivers,
        "active_drivers": active_drivers,
        "available_drivers": available_drivers,
        "busy_drivers": busy_drivers,


        "total_vehicles": total_vehicles,
        "active_vehicles": active_vehicles,
        "available_vehicles": available_vehicles,
        "vehicles_in_use": vehicles_in_use,
        "vehicles_in_maintenance":
            vehicles_in_maintenance,

        "vehicle_utilization":
            vehicle_utilization,


        "total_deliveries":
            total_deliveries,

        "pending_deliveries":
            pending_deliveries,

        "active_deliveries":
            active_deliveries,

        "assigned_deliveries":
            assigned_deliveries,

        "in_transit_deliveries":
            in_transit_deliveries,

        "delivered_deliveries":
            delivered_deliveries,

        "completed_deliveries":
            delivered_deliveries,

        "cancelled_deliveries":
            cancelled_deliveries,


        "average_delivery_time_minutes":
            average_delivery_time,

        "top_performing_drivers":
            top_performing_drivers,

        "delivery_success_rate":
            delivery_success_rate
    }

    # Save Dashboard in Redis for 60 seconds
            # Save Dashboard in Redis for 60 seconds

    print("Saving Dashboard To Redis...")

    redis_client.setex(
        "analytics_dashboard",
        60,
        json.dumps(dashboard_data)
    )

    print("Saved Successfully!")

    return dashboard_data
def get_driver_analytics(db: Session):

    drivers = db.query(Driver).all()

    result = []

    for driver in drivers:

        total = (
            db.query(Delivery)
            .filter(
                Delivery.driver_id == driver.id
            )
            .count()
        )

        completed = (
            db.query(Delivery)
            .filter(
                Delivery.driver_id == driver.id,
                Delivery.status == DeliveryStatus.DELIVERED
            )
            .count()
        )

        cancelled = (
            db.query(Delivery)
            .filter(
                Delivery.driver_id == driver.id,
                Delivery.status == DeliveryStatus.CANCELLED
            )
            .count()
        )

        result.append(
            {
                "driver_id": driver.id,
                "driver_name": driver.name,
                "total_deliveries": total,
                "completed_deliveries": completed,
                "cancelled_deliveries": cancelled
            }
        )

    return result


def get_delivery_analytics(db: Session):

    return {

        "total_deliveries":
            db.query(Delivery).count(),

        "pending_deliveries":
            db.query(Delivery)
            .filter(
                Delivery.status == DeliveryStatus.PENDING
            )
            .count(),

        "assigned_deliveries":
            db.query(Delivery)
            .filter(
                Delivery.status == DeliveryStatus.ASSIGNED
            )
            .count(),

        "picked_up_deliveries":
            db.query(Delivery)
            .filter(
                Delivery.status == DeliveryStatus.PICKED_UP
            )
            .count(),

        "in_transit_deliveries":
            db.query(Delivery)
            .filter(
                Delivery.status == DeliveryStatus.IN_TRANSIT
            )
            .count(),

        "delivered_deliveries":
            db.query(Delivery)
            .filter(
                Delivery.status == DeliveryStatus.DELIVERED
            )
            .count(),

        "cancelled_deliveries":
            db.query(Delivery)
            .filter(
                Delivery.status == DeliveryStatus.CANCELLED
            )
            .count()
    }