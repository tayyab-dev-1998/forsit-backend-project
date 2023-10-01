from fastapi import APIRouter

from api import login_api

api_router = APIRouter()

api_router.include_router(login_api.router, tags=["login"])
