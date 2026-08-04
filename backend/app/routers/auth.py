from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token
)

from app.database import get_db

from app.schemas.user import (
    UserRegister,
    TokenResponse,
    UserResponse
)

from app.services.auth_service import (
    register_user,
    authenticate_user,
    create_tokens
)

from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# -------------------------
# Register User
# -------------------------

@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    new_user = register_user(
        db,
        user
    )

    if not new_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return new_user



# -------------------------
# Login User
# -------------------------

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )


    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    return create_tokens(db_user)



# -------------------------
# Refresh Token
# -------------------------

@router.post("/refresh")
def refresh_token(
    refresh_token: str
):

    try:

        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[
                settings.ALGORITHM
            ]
        )


        # check token type

        if payload.get("type") != "refresh":

            raise HTTPException(
                status_code=401,
                detail="Invalid token type"
            )


        user_id = payload.get("sub")


        if user_id is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )


        new_access_token = create_access_token(
            {
                "sub": user_id
            }
        )


        new_refresh_token = create_refresh_token(
            {
                "sub": user_id
            }
        )


        return {

            "access_token": new_access_token,

            "refresh_token": new_refresh_token,

            "token_type": "bearer"
        }


    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )



# -------------------------
# Current User
# -------------------------

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user = Depends(get_current_user)
):

    return current_user