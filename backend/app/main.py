from fastapi import FastAPI

from app.routers import (
    auth,
    admin,
    drivers,
    driver,
    vehicles,
    deliveries,
    analytics,
    tracking,
    websocket,
    notifications,
    assignments,
    route
)

app = FastAPI(
    title="Fleet & Delivery Management API",
    version="1.0.0",
    description="Backend API for Fleet & Delivery Management Platform"
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(drivers.router)
app.include_router(driver.router)
app.include_router(vehicles.router)
app.include_router(deliveries.router)
app.include_router(analytics.router)
app.include_router(tracking.router)
app.include_router(websocket.router)
app.include_router(notifications.router)
app.include_router(assignments.router)
app.include_router(route.router)


@app.get("/")
def root():
    return {
        "message": "Fleet & Delivery Management API is running successfully!"
    }