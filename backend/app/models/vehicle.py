from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SqlEnum,
    Integer,
    String
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class VehicleStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    IN_USE = "IN_USE"
    MAINTENANCE = "MAINTENANCE"



class Vehicle(Base):

    __tablename__ = "vehicles"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )


    vehicle_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )


    vehicle_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )


    capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    fuel_type: Mapped[str] = mapped_column(
    String(30),
    nullable=False,
    default="DIESEL"
     )

    status: Mapped[VehicleStatus] = mapped_column(
        SqlEnum(VehicleStatus),
        default=VehicleStatus.AVAILABLE,
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


    # Relationship with Driver
    driver = relationship(
        "Driver",
        back_populates="vehicle",
        uselist=False
    )