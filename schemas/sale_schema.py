from datetime import date
from enum import Enum

from pydantic import BaseModel, validator


# Shared properties
class SaleBase(BaseModel):
    quantity_sold: int
    sales_date: date
    product_id: int

    @validator("quantity_sold")
    def quantity_sold_must_be_greater_then_zero(cls, v):
        if v <= 0:
            raise ValueError("Quantity sold should be greater than 0.")
        return v


# Properties to receive on sale creation
class SaleCreate(SaleBase):
    pass


# Properties shared by models stored in DB
class SaleInDbBase(SaleBase):
    id: int
    item_sold_at: int
    total_bill: int

    class Config:
        orm_mode = True


# Properties to return to client
class Sale(SaleInDbBase):
    pass


# Filter type for get api to get entity to perform filter on
class SaleFilter(str, Enum):
    category = "category"
    product = "product"
