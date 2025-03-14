from fastapi import APIRouter
from app.controllers import smoke
from app.controllers import chat
from app.controllers import login

api_v1 = APIRouter()

api_v1.include_router(router=smoke.router, prefix="/smoke", tags=["Smoke"])
api_v1.include_router(router=chat.router, prefix="/chat")
api_v1.include_router(router=login.router, prefix="/login")
