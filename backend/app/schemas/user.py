from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


class UserRegister(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6
    )

    role: UserRole = UserRole.DRIVER



class UserLogin(BaseModel):

    email: EmailStr

    password: str



class TokenResponse(BaseModel):

    access_token: str

    refresh_token: str

    token_type: str = "bearer"



class UserResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime


    class Config:
        from_attributes = True