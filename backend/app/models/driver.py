from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SqlEnum,
    String,
    ForeignKey
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class DriverStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    BUSY = "BUSY"
    OFFLINE = "OFFLINE"


class Driver(Base):

    __tablename__ = "drivers"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )


    # Link Driver with User table
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )


    # Link Driver with Vehicle table
    vehicle_id: Mapped[int | None] = mapped_column(
        ForeignKey("vehicles.id"),
        nullable=True
    )


    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


    phone_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )


    license_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )


    status: Mapped[DriverStatus] = mapped_column(
        SqlEnum(DriverStatus),
        default=DriverStatus.AVAILABLE,
        nullable=False
    )


    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


    # Relationship with User
    user = relationship(
        "User",
        back_populates="driver"
    )


    # Relationship with Vehicle
    vehicle = relationship(
        "Vehicle",
        back_populates="driver"
    )