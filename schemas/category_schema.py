from pydantic import BaseModel


# Shared properties
class CategoryBase(BaseModel):
    name: str


# Properties to receive on category creation
class CategoryCreate(CategoryBase):
    pass


# Properties shared by models stored in DB
class CategoryInDbBase(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Category(CategoryInDbBase):
    pass
