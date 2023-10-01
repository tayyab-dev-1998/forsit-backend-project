from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dep import authenticate_request
from db.session import get_db
from schemas.category_schema import Category, CategoryCreate
from services.category_services import create_category, get_categories

router = APIRouter()


@router.post("/", response_model=Category, dependencies=[Depends(authenticate_request)])
def create(
    category: CategoryCreate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Create new Category.
    """
    category = create_category(db, category)
    return category


@router.get(
    "/", response_model=List[Category], dependencies=[Depends(authenticate_request)]
)
def get_all(
    db: Session = Depends(get_db),
) -> Any:
    """
    List all Categories.
    """
    categories = get_categories(db)
    return categories
