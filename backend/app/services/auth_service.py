from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserRegister

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)


def register_user(
    db: Session,
    user_data: UserRegister
):

    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        return None


    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(
            user_data.password
        ),
        role=user_data.role
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


    if not user:
        return None


    if not verify_password(
        password,
        user.password_hash
    ):
        return None


    return user



def create_tokens(user):

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role
        }
    )


    refresh_token = create_refresh_token(
        {
            "sub": str(user.id)
        }
    )


    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }