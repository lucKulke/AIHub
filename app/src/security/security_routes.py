from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Security
from .handler import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_active_user,
)
from .security_schemas import User, NewUser, Token
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm

from ..db import crud
from ..db.database_connection import get_db
from sqlalchemy.orm import Session


router = APIRouter(tags=["Security"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "scopes": user.scopes,
        },
        expires_delta=access_token_expires,
    )
    print(type(minutes_to_timestamp(ACCESS_TOKEN_EXPIRE_MINUTES)), flush=True)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_at": minutes_to_timestamp(ACCESS_TOKEN_EXPIRE_MINUTES),
    }


def minutes_to_timestamp(minutes):
    current_time = datetime.utcnow()
    expiration_time = current_time + timedelta(minutes=minutes)
    return expiration_time.timestamp()


@router.post("/create_user/", response_model=User)
async def create_user(
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["create_user"])
    ],
    new_user: NewUser,
    db: Session = Depends(get_db),
):
    user = crud.get_user(db, new_user.username)
    if user:
        raise HTTPException(status_code=403, detail="already exits")

    user = crud.create_user(db, new_user)
    db.commit()

    return user


@router.post("/disable_user/", response_model=User)
async def disable_user(
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["disable_user"])
    ],
    username: str,
    db: Session = Depends(get_db),
):
    user = crud.disable_user(db, username)
    if user:
        db.commit()
        return user

    raise HTTPException(status_code=404, detail="user does not exist.")
