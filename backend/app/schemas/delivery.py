from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class DeliveryStatus(str, Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    DELAYED = "DELAYED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class DeliveryPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class DeliveryCreate(BaseModel):

    tracking_number: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    customer_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    pickup_address: str = Field(
        ...,
        min_length=3,
        max_length=255
    )

    delivery_address: str = Field(
        ...,
        min_length=3,
        max_length=255
    )

    package_weight: float = Field(
        ...,
        gt=0
    )

    priority: DeliveryPriority

    scheduled_time: datetime


class DeliveryUpdate(BaseModel):

    customer_name: str | None = None
    pickup_address: str | None = None
    delivery_address: str | None = None
    package_weight: int | None = None
    priority: DeliveryPriority | None = None
    scheduled_time: datetime | None = None
    status: DeliveryStatus | None = None
    driver_id: int | None = None


class DeliveryResponse(BaseModel):

    id: int
    tracking_number: str
    customer_name: str
    pickup_address: str
    delivery_address: str
    package_weight: int
    priority: DeliveryPriority
    scheduled_time: datetime
    status: DeliveryStatus
    driver_id: int | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class DriverDeliveryResponse(BaseModel):

    id: int
    tracking_number: str
    customer_name: str
    pickup_address: str
    delivery_address: str
    package_weight: int
    priority: DeliveryPriority
    scheduled_time: datetime
    status: DeliveryStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class DeliveryStatusUpdate(BaseModel):
    status: DeliveryStatus