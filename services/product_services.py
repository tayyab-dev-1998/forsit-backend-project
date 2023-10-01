from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models.product_model import Product
from schemas.product_schema import ProductCreate
from services.category_services import get_category_by_id


def get_product_by_id(db: Session, id: int, raise_if_none=False):
    object = db.query(Product).filter(Product.id == id).first()
    if object is None and raise_if_none:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product doesn't exists.",
        )
    return object


def create_product(db: Session, payload: ProductCreate):
    get_category_by_id(db, payload.category_id, raise_if_none=True)
    data = jsonable_encoder(payload)
    product = Product(**data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(db: Session):
    products = db.query(Product).all()
    return products
