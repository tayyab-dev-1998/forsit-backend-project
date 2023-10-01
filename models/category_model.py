from sqlalchemy import Column, String

from models.base_model import BaseModel


class Category(BaseModel):
    name = Column(String, unique=True, nullable=False)
