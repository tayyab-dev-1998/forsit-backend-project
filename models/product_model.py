from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.constants import DEFAULT_LOW_QUANTITY_THRESHOLD
from models.base_model import BaseModel


class Product(BaseModel):
    name = Column(String, nullable=False)
    product_sku = Column(String, unique=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    low_quantity_threshold = Column(
        Integer, default=DEFAULT_LOW_QUANTITY_THRESHOLD, nullable=False
    )

    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    category = relationship("Category", back_populates="products")
