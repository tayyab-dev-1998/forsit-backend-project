from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from core.config import settings
from core.constants import JWT_ALGORITHM
from models.user_model import User
from services.common_services import verify_password


def create_access_token(subject: Union[str, Any]) -> str:
    expires_delta = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt


def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    return user


def get_user_access_token(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    hashed_pass = user.hashed_password
    if not verify_password(password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    return create_access_token(user.email)
