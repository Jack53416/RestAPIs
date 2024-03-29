from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_user
from app.core import config
from app.core.jwt import create_user_access_token
from app.models.user import User as DBUser
from app.resources import strings
from app.schemas.token import Token
from app.schemas.user import User

router = APIRouter()


@router.post("/access-token",
             response_model=Token,
             name='login:create-token')
def login_access_token(
        db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=strings.INVALID_EMAIL_PASSWORD,
                            headers={"WWW-Authenticate": "Bearer"})
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strings.USER_INACTIVE)
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_user_access_token(user, access_token_expires),
        "token_type": "bearer",
    }


@router.post("/verify-token",
             response_model=User,
             name='login:verify-token')
def verify_token(current_user: DBUser = Depends(get_current_user)):
    """
    Test access token
    """

    return current_user
