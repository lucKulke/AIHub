from sqlalchemy import Column, Integer, String
from .database import Base


class Applications(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
