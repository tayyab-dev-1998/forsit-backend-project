from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dep import authenticate_request
from db.session import get_db
from schemas.category_schema import Category, CategoryCreate
from services.category_services import create_category

router = APIRouter()


@router.post("/", response_model=Category, dependencies=[Depends(authenticate_request)])
def create_item(
    category: CategoryCreate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Create new Category.
    """
    category = create_category(db, category)
    return category
