from sqlalchemy import Column, String

from models.base_model import BaseModel


class User(BaseModel):
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
