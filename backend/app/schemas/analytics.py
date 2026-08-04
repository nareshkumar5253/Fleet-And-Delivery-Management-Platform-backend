from typing import List

from pydantic import BaseModel


class TopDriverResponse(BaseModel):
    driver_id: int
    driver_name: str
    completed_deliveries: int


class DashboardResponse(BaseModel):

    total_drivers: int
    active_drivers: int
    available_drivers: int
    busy_drivers: int

    total_vehicles: int
    active_vehicles: int
    available_vehicles: int
    vehicles_in_use: int
    vehicles_in_maintenance: int

    vehicle_utilization: float

    total_deliveries: int
    pending_deliveries: int
    active_deliveries: int
    assigned_deliveries: int
    in_transit_deliveries: int
    delivered_deliveries: int
    completed_deliveries: int
    cancelled_deliveries: int

    average_delivery_time_minutes: float

    top_performing_drivers: List[TopDriverResponse]

    delivery_success_rate: float


class DriverAnalyticsResponse(BaseModel):
    driver_id: int
    driver_name: str
    total_deliveries: int
    completed_deliveries: int
    cancelled_deliveries: int


class DeliveryAnalyticsResponse(BaseModel):
    total_deliveries: int
    pending_deliveries: int
    assigned_deliveries: int
    picked_up_deliveries: int
    in_transit_deliveries: int
    delivered_deliveries: int
    cancelled_deliveries: int