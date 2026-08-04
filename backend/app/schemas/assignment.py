from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AssignmentCreate(BaseModel):

    delivery_id: int

    driver_id: int

    vehicle_id: int | None = None

    estimated_distance: float | None = None

    estimated_time: float | None = None



class AssignmentResponse(BaseModel):

    id: int

    delivery_id: int

    driver_id: int

    vehicle_id: int | None

    assigned_at: datetime

    estimated_distance: float | None

    estimated_time: float | None


    model_config = ConfigDict(
        from_attributes=True
    )