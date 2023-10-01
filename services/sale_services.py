from datetime import date

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from models.sale_model import Sale
from schemas.sale_schema import SaleAggregationType, SaleCreate, SaleFilter
from services.product_services import get_product_by_id


def create_sale_entry(db: Session, sale_data: SaleCreate):
    product = get_product_by_id(db, sale_data.product_id, raise_if_none=True)
    if product.quantity < sale_data.quantity_sold:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product doesn't have enough quantity left in inventory.",
        )
    product.quantity = product.quantity - sale_data.quantity_sold
    data = jsonable_encoder(sale_data)
    sale_entry = Sale(**data)
    sale_entry.item_sold_at = product.price
    sale_entry.total_bill = sale_entry.quantity_sold * sale_entry.item_sold_at

    db.add(product)
    db.add(sale_entry)
    db.commit()
    return sale_entry


def get_total_sales_for_category(
    db: Session, category_id: int, start_date: date, end_date: date
):
    total_sales = (
        db.query(func.sum(Sale.total_bill))
        .filter(Sale.product.has(category_id=category_id))
        .filter(Sale.sales_date >= start_date)
        .filter(Sale.sales_date <= end_date)
    )
    return total_sales.first()[0]


def fetch_sale_entries(
    db: Session,
    filter_id: int,
    start_date: date,
    end_date: date,
    filter_type: SaleFilter,
):
    query = (
        db.query(Sale)
        .filter(Sale.sales_date >= start_date)
        .filter(Sale.sales_date <= end_date)
    )
    if filter_type == SaleFilter.product:
        query.filter(Sale.product_id == filter_id)
    else:
        query.filter(Sale.product.has(category_id=filter_id))
    return query.all()


def perform_sale_aggregation(
    db: Session,
    aggregation_type: SaleAggregationType,
):
    query = db.query(
        func.date_trunc(aggregation_type.value, Sale.sales_date).label("sales_date"),
        func.sum(Sale.total_bill).label("revenue"),
    ).group_by("sales_date")
    result = {}
    for row in query.all():
        result[row.sales_date] = row.revenue
    return result
