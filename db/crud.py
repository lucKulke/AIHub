from sqlalchemy.orm import Session

from . import models


def add_application(db: Session, app_name: str, id: int):
    new_app = models.Applications(name=app_name, id=id)
    db.add(new_app)
    db.commit()
    return True
