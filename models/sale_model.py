from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Sale(BaseModel):
    quantity_sold = Column(Integer, nullable=False)
    total_bill = Column(Integer, nullable=False)
    item_sold_at = Column(Integer, nullable=False)
    sales_date = Column(Date, index=True)

    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product", back_populates="sales")
