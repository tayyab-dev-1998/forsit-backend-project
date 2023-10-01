from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dep import authenticate_request
from db.session import get_db
from schemas.product_schema import Product, ProductCreate
from services.product_services import (create_product, get_product_by_id,
                                       get_products)

router = APIRouter()


@router.post("/", response_model=Product, dependencies=[Depends(authenticate_request)])
def create(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Create new Product.
    """
    product = create_product(db, product_data)
    return product


@router.get(
    "/", response_model=List[Product], dependencies=[Depends(authenticate_request)]
)
def get_all(
    db: Session = Depends(get_db),
) -> Any:
    """
    List all Products.
    """
    products = get_products(db)
    return products


@router.get(
    "/{id}", response_model=Product, dependencies=[Depends(authenticate_request)]
)
def get(
    id: int,
    db: Session = Depends(get_db),
):
    """
    Get product by id.
    """
    product = get_product_by_id(db, id, raise_if_none=True)
    return product
