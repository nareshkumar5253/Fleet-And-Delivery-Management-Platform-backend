from sqlalchemy.orm import Session

from app.models.delivery import Delivery, DeliveryStatus


def optimize_route(
    db: Session,
    driver_id: int
):
    deliveries = (
        db.query(Delivery)
        .filter(
            Delivery.driver_id == driver_id,
            Delivery.status.in_(
                [
                    DeliveryStatus.ASSIGNED,
                    DeliveryStatus.PICKED_UP,
                    DeliveryStatus.IN_TRANSIT,
                ]
            )
        )
        .order_by(Delivery.priority.desc())
        .all()
    )

    route = []

    stop = 1

    for delivery in deliveries:

        route.append(
            {
                "stop": stop,
                "delivery_id": delivery.id,
                "tracking_number": delivery.tracking_number,
                "pickup": delivery.pickup_address,
                "destination": delivery.delivery_address,
                "priority": delivery.priority,
            }
        )

        stop += 1

    return {
        "driver_id": driver_id,
        "total_stops": len(route),
        "optimized_route": route,
    }