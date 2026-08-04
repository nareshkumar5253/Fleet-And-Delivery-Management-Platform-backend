from datetime import datetime

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class DeliveryStatusHistory(Base):

    __tablename__ = "delivery_status_history"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    delivery_id: Mapped[int] = mapped_column(
        ForeignKey("deliveries.id"),
        nullable=False
    )

    old_status: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    new_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    changed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )