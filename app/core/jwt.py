from datetime import datetime, timedelta

import jwt

from app.core import config
from app.schemas import User

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')
    return encoded_jwt


def create_user_access_token(user: User, expires_delta: timedelta = None):
    return create_access_token(
        data={"user_id": user.id},
        expires_delta=expires_delta
    )
