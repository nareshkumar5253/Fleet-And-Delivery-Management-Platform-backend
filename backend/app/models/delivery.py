from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class DeliveryStatus(str, Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    DELAYED =   "DELAYED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class DeliveryPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    tracking_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    customer_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    pickup_address: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    delivery_address: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    package_weight: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    priority: Mapped[DeliveryPriority] = mapped_column(
        SqlEnum(DeliveryPriority),
        default=DeliveryPriority.MEDIUM,
        nullable=False
    )

    scheduled_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    status: Mapped[DeliveryStatus] = mapped_column(
    SqlEnum(
        DeliveryStatus,
        name="deliverystatus",
        native_enum=True,
        validate_strings=True
    ),
    default=DeliveryStatus.PENDING,
    nullable=False
     )

    driver_id: Mapped[int | None] = mapped_column(
        ForeignKey("drivers.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )