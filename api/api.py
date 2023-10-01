from fastapi import APIRouter

from api import category_api, login_api

api_router = APIRouter()

api_router.include_router(login_api.router, tags=["login"])
api_router.include_router(category_api.router, prefix="/categories", tags=["category"])
