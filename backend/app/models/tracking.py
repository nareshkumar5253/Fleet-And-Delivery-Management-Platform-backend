from datetime import datetime

from sqlalchemy import (
    Float,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class TrackingHistory(Base):

    __tablename__ = "tracking_history"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )


    delivery_id: Mapped[int] = mapped_column(
        ForeignKey("deliveries.id"),
        nullable=False
    )


    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )


    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )


    location: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


    speed: Mapped[float] = mapped_column(
        Float,
        default=0
    )


    delivery_status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING"
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )