from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User, UserRole
from app.models.delivery import Delivery


router = APIRouter(
    prefix="/driver",
    tags=["Driver"]
)


@router.get("/deliveries")
def get_my_deliveries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != UserRole.DRIVER:
        raise HTTPException(
            status_code=403,
            detail="Only drivers can access this"
        )


    return (
        db.query(Delivery)
        .filter(
            Delivery.driver_id == current_user.driver.id
        )
        .all()
    )
from sqlalchemy.orm import relationship


vehicle = relationship(
    "Vehicle",
    back_populates="drivers"
)