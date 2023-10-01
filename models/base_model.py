from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

from db.base_class import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
