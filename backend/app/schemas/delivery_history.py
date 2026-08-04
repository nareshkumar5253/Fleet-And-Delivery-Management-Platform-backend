from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DeliveryStatusHistoryResponse(BaseModel):

    id: int

    delivery_id: int

    old_status: str | None

    new_status: str

    changed_at: datetime


    model_config = ConfigDict(
        from_attributes=True
    )