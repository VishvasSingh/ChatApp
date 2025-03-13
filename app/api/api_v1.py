from fastapi import APIRouter
from app.services.controllers import smoke


api_v1 = APIRouter()

api_v1.include_router(router=smoke.router, prefix='/smoke', tags=["Smoke"])
