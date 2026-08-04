from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.roles import require_admin

from app.schemas.analytics import (
    DashboardResponse,
    DriverAnalyticsResponse,
    DeliveryAnalyticsResponse
)

from app.services.analytics_service import (
    get_dashboard,
    get_driver_analytics,
    get_delivery_analytics
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get(
    "/dashboard",
    response_model=DashboardResponse
)
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):
    return get_dashboard(db)


@router.get(
    "/drivers",
    response_model=List[DriverAnalyticsResponse]
)
def drivers(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):
    return get_driver_analytics(db)


@router.get(
    "/deliveries",
    response_model=DeliveryAnalyticsResponse
)
def deliveries(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin())
):
    return get_delivery_analytics(db)