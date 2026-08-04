from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DriverStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    BUSY = "BUSY"
    OFFLINE = "OFFLINE"


# -------------------------
# Vehicle Info inside Driver
# -------------------------

class VehicleInfo(BaseModel):

    id: int

    vehicle_number: str

    vehicle_type: str

    capacity: int


    model_config = ConfigDict(
        from_attributes=True
    )


# -------------------------
# Create Driver
# -------------------------

class DriverCreate(BaseModel):

    user_id: int

    name: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    phone_number: str

    license_number: str



# -------------------------
# Update Driver
# -------------------------

class DriverUpdate(BaseModel):

    name: Optional[str] = None

    phone_number: Optional[str] = None

    license_number: Optional[str] = None

    status: Optional[DriverStatus] = None

    is_active: Optional[bool] = None

    vehicle_id: Optional[int] = None



# -------------------------
# Driver Response
# -------------------------

class DriverResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )


    id: int

    user_id: int

    name: str

    phone_number: str

    license_number: str


    status: DriverStatus

    is_active: bool


    vehicle_id: Optional[int] = None


    vehicle: Optional[VehicleInfo] = None


    created_at: datetime