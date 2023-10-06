from sqlalchemy import Column, Integer, String
from .database_connection import Base


class Applications(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
