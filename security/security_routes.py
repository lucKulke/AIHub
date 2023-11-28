from datetime import datetime, timedelta
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Security
import os
from .handler import (
    verify_password,
    get_password_hash,
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_active_user,
    fake_users_db,
)
from .schemas import UserInDB, User, NewUser, UserInDB, TokenData, Token
from typing import Annotated

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)


router = APIRouter(tags=["Security"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
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
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create_user/")
async def read_own_items(
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["create_user"])
    ],
    new_user: NewUser,
):
    if new_user.username in fake_users_db:
        raise HTTPException(status_code=403, detail="already exits")

    new_user_dict = dict(new_user)
    hashed_password = get_password_hash(new_user.password)
    new_user_dict["hashed_password"] = hashed_password
    del new_user_dict["password"]
    fake_users_db[new_user.username] = new_user_dict
    return {"new_user": new_user_dict, "db": fake_users_db}
