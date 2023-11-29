from sqlalchemy.orm import Session
from fastapi import Depends

from . import models
from utilitys.hashing import get_password_hash
from security.security_schemas import NewUser

scopes_list_to_string = lambda l: ",".join(l)


def create_admin(db: Session, new_user: NewUser):
    user = get_user(db, new_user.username)
    if not user:
        create_user(db, new_user)
        return "new admin created!"
    return update_admin_scopes(user, new_user.scopes)


def create_user(db: Session, new_user: NewUser):
    user = models.Users(
        username=new_user.username,
        password=get_password_hash(new_user.password),
        disabled=new_user.disabled,
        scopes=scopes_list_to_string(new_user.scopes),
    )
    db.add(user)
    return user


def update_admin_scopes(user: models.Users, scopes: str):
    scopes_string = scopes_list_to_string(scopes)
    if user.scopes != scopes_string:
        user.scopes = scopes_string
        return "scopes of existing admin updated!"
    return "no admin changes!"


def get_user(db: Session, username: str):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    return user


def disable_user(db: Session, username: str):
    user = get_user(db, username)
    if user:
        user.disabled = True
        return user
    return False
