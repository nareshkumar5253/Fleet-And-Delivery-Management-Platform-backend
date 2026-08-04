from datetime import datetime
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class VehicleStatus(str, Enum):

    AVAILABLE = "AVAILABLE"
    IN_USE = "IN_USE"
    MAINTENANCE = "MAINTENANCE"



class VehicleCreate(BaseModel):

    vehicle_number: str = Field(
        ...,
        min_length=3,
        max_length=20
    )


    vehicle_type: str = Field(
        ...,
        min_length=3,
        max_length=50
    )


    capacity: int = Field(
        ...,
        gt=0
    )


    fuel_type: str = Field(
        ...,
        min_length=2,
        max_length=30
    )



class VehicleUpdate(BaseModel):

    vehicle_number: str | None = None

    vehicle_type: str | None = None

    capacity: int | None = None

    fuel_type: str | None = None

    status: VehicleStatus | None = None

    is_active: bool | None = None



class VehicleResponse(BaseModel):

    id: int

    vehicle_number: str

    vehicle_type: str

    capacity: int

    fuel_type: str

    status: VehicleStatus

    is_active: bool

    created_at: datetime


    model_config = ConfigDict(
        from_attributes=True
    )