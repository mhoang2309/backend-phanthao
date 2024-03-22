from fastapi import APIRouter

from app.api.v1.endpoints import api_user

api = APIRouter()

api.include_router(api_user, tags=["API Manage"])
