#  Fleet & Delivery Management Platform

A scalable backend platform built with **FastAPI** for managing fleet operations, delivery assignments, real-time tracking, notifications, and analytics.

This project provides a complete solution for businesses to manage drivers, vehicles, deliveries, and live tracking with secure authentication and background task processing.

---

#  Features

##  Authentication & Authorization

- User Registration
- User Login
- JWT Access Token
- Refresh Token
- Role-Based Access Control
- Secure Password Hashing

### Supported Roles

- Admin
- Dispatcher
- Driver

---

#  Driver Management

- Create Driver
- Update Driver
- Suspend Driver
- Driver Availability Status
- Assign Vehicle
- View Driver Deliveries

---

#  Vehicle Management

- Add Vehicle
- Update Vehicle
- Delete Vehicle
- Vehicle Status
- Vehicle Capacity
- Fuel Type
- Vehicle Assignment

---

#  Delivery Management

- Create Delivery
- Update Delivery
- Delete Delivery
- Delivery History
- Delivery Priority
- Delivery Status
- Scheduled Deliveries

Supported Statuses

- Pending
- Assigned
- Picked Up
- In Transit
- Delivered
- Cancelled

---

#  Route Assignment

- Assign Driver
- Assign Vehicle
- Reassign Delivery
- Estimated Distance
- Estimated Delivery Time
- Route Optimization

---

#  Real-Time Delivery Tracking

Implemented using **WebSockets**

Supports

- Live Driver Location
- Latitude
- Longitude
- Speed
- Delivery Status Updates
- Instant Dispatcher Notifications

---

#  Notification System

Notifications generated for

- Delivery Assigned
- Driver Started Trip
- Delivery Delayed
- Delivery Completed
- Delivery Cancelled

Background notifications processed using **Celery**.

---

# 📊 Analytics Dashboard

Analytics APIs include

- Total Deliveries
- Pending Deliveries
- Active Deliveries
- Completed Deliveries
- Cancelled Deliveries
- Active Drivers
- Vehicle Utilization
- Average Delivery Time
- Delivery Success Rate
- Top Performing Drivers

---

#  Background Task Processing

Implemented using

- Celery
- Redis

Used for

- Delivery Notifications
- Background Processing
- Asynchronous Tasks

---

#  Testing

Project contains test cases for

- Authentication
- Drivers
- Deliveries

---

# 🛠 Tech Stack

| Technology | Description |
|------------|-------------|
| Python | Programming Language |
| FastAPI | Backend Framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Alembic | Database Migration |
| JWT | Authentication |
| Redis | Caching |
| Celery | Background Jobs |
| WebSockets | Real-Time Tracking |
| Docker | Containerization |
| Pytest | Testing |

---

#  Project Structure

```
backend
│
├── alembic
├── app
│   ├── core
│   ├── database
│   ├── dependencies
│   ├── models
│   ├── routers
│   ├── schemas
│   ├── services
│   ├── websocket
│   ├── worker
│   ├── tasks
│   └── main.py
│
├── tests
├── Dockerfile
├── requirements.txt
└── docker-compose.yml
```

---

#  Installation

## Clone Repository

```bash
git clone https://github.com/nareshkumar5253/Fleet-And-Delivery-Management-Platform-backend.git

cd Fleet-And-Delivery-Management-Platform
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file inside the backend folder.

Example

```env
DATABASE_URL=postgresql://postgres:Naresh5253@localhost:5432/fleet_db

SECRET_KEY=ThisIsMyVerySecretKey123456

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7

REDIS_URL=redis://localhost:6379/0
```

---

## Run Database Migration

```bash
cd backend

alembic upgrade head
```

---

## Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

API Documentation

```
http://127.0.0.1:8000/docs
```

---

## Start Redis

```bash
redis-server
```

---

## Start Celery Worker

```bash
celery -A app.worker.celery_app worker --loglevel=info
```

---

#  Docker

Build

```bash
docker-compose build
```

Run

```bash
docker-compose up
```

---

# 🔌 Main API Endpoints

## Authentication

```
POST /auth/register

POST /auth/login

POST /auth/refresh

GET /auth/me
```

---

## Drivers

```
POST /drivers

GET /drivers

GET /drivers/{id}

PUT /drivers/{id}

DELETE /drivers/{id}
```

---

## Vehicles

```
POST /vehicles

GET /vehicles

PUT /vehicles/{id}

DELETE /vehicles/{id}
```

---

## Deliveries

```
POST /deliveries

GET /deliveries

GET /deliveries/{id}

PUT /deliveries/{id}

DELETE /deliveries/{id}
```

---

## Assignments

```
POST /assignments

GET /route/optimize/{driver_id}
```

---

## Tracking

```
POST /tracking/location

GET /tracking/{delivery_id}
```

WebSocket

```
ws://localhost:8000/ws/tracking/{delivery_id}
```

---

## Analytics

```
GET /analytics/dashboard

GET /analytics/drivers

GET /analytics/deliveries
```

---

#  Security

- JWT Authentication
- Refresh Tokens
- Password Hashing
- Role-Based Authorization
- Protected APIs

---

#  Future Enhancements

- Google Maps Route Optimization
- GPS Integration
- SMS Notifications
- Email Notifications
- Push Notifications
- AI-Based Route Prediction
- Driver Performance Prediction
- Delivery ETA Prediction

----
