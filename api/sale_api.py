from datetime import date
from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dep import authenticate_request
from db.session import get_db
from schemas.sale_schema import Sale, SaleCreate, SaleFilter
from services.sale_services import (
    create_sale_entry,
    fetch_sale_entries,
    get_total_sales_for_category,
)

router = APIRouter()


@router.post("/", response_model=Sale, dependencies=[Depends(authenticate_request)])
def create(
    sale_data: SaleCreate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Create new Sale.
    """
    sale = create_sale_entry(db, sale_data)
    return sale


@router.get(
    "/category/{category_id}/revenue", dependencies=[Depends(authenticate_request)]
)
def get_revenue_for_category(
    category_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
):
    return get_total_sales_for_category(db, category_id, start_date, end_date)


@router.get(
    "/", response_model=List[Sale], dependencies=[Depends(authenticate_request)]
)
def get_sales_entry(
    filter_type: SaleFilter,
    filter_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
):
    return fetch_sale_entries(db, filter_id, start_date, end_date, filter_type)
