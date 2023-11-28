from sqlalchemy.orm import Session
from fastapi import Depends

from . import models
from security.handler import get_password_hash


def create_admin(
    db: Session,
    username: str,
    password: str,
    scopes: str,
):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        admin_user = models.Users(
            username=username,
            password=get_password_hash(password),
            disabled=False,
            scopes=scopes,
        )
        db.add(admin_user)
        return "new admin created!"
    return update_admin_scopes(user, scopes)


def update_admin_scopes(user: models.Users, scopes: str):
    if user.scopes != scopes:
        user.scopes = scopes
        return "scopes of existing admin updated!"
    return "no admin changes!"
