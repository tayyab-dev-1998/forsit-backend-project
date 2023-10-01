from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models.category_model import Category
from schemas.category_schema import CategoryCreate


def get_category_by_name(db: Session, name: str, raise_if_none=False):
    object = db.query(Category).filter(Category.name == name).first()
    if object is None and raise_if_none:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category doesn't exists.",
        )
    return object


def create_category(db: Session, payload: CategoryCreate):
    category = get_category_by_name(db, payload.name)
    if category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists. Id={}.".format(category.id),
        )

    category_data = jsonable_encoder(payload)
    category = Category(**category_data)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
