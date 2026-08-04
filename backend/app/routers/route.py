from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.roles import require_admin

from app.services.route_service import optimize_route

router = APIRouter(
    prefix="/route",
    tags=["Route Assignment"]
)


@router.get("/optimize/{driver_id}")
def optimize(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):
    return optimize_route(
        db,
        driver_id
    )