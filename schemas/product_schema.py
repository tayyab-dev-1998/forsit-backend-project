from typing import Optional

from pydantic import BaseModel, validator

from core.constants import DEFAULT_LOW_QUANTITY_THRESHOLD


# Shared properties
class ProductBase(BaseModel):
    name: str
    product_sku: str
    quantity: int
    category_id: int
    price: int
    low_quantity_threshold: Optional[int] = DEFAULT_LOW_QUANTITY_THRESHOLD

    @validator("quantity")
    def quantity_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Quantity cannot be negative.")
        return v

    @validator("price")
    def price_must_be_greater_then_zero(cls, v):
        if v <= 0:
            raise ValueError("Price should be greater than 0.")
        return v


# Properties to receive on product creation
class ProductCreate(ProductBase):
    pass


# Properties shared by models stored in DB
class ProductInDbBase(ProductBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Product(ProductInDbBase):
    pass
