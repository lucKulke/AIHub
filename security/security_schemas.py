from pydantic import BaseModel, ValidationError, ConfigDict


class User(BaseModel):
    username: str
    disabled: bool | None = None


class NewUser(User):
    password: str
    scopes: list


class UserInDB(User):
    password: str
    scopes: list


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
