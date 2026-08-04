from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey
)

from app.database import Base


class DeliveryAssignment(Base):

    __tablename__ = "delivery_assignments"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    delivery_id = Column(
        Integer,
        ForeignKey("deliveries.id"),
        nullable=False
    )


    driver_id = Column(
        Integer,
        ForeignKey("drivers.id"),
        nullable=False
    )


    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id"),
        nullable=True
    )


    assigned_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    estimated_distance = Column(
        Float,
        nullable=True
    )


    # Time in hours
    estimated_time = Column(
        Float,
        nullable=True
    )