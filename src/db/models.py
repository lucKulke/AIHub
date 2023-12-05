from sqlalchemy import Column, Integer, String, Boolean
from .database_connection import Base


class Users(Base):
    __tablename__ = "users"

    username = Column(String(100), primary_key=True, index=True)
    password = Column(String(100))
    disabled = Column(Boolean)
    scopes = Column(String)

    class Config:
        orm_mode = True
