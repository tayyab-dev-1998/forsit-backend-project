from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Category(BaseModel):
    name = Column(String, unique=True, nullable=False)
    products = relationship("Product", back_populates="category")
