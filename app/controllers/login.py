from fastapi import APIRouter, Depends
from app.auth.jwt_handler import create_access_token
from app.auth.dependencies import get_current_user
from app.schemas.login import LoginRequest

router = APIRouter()


@router.post("")
async def login(login_request: LoginRequest):
    token = create_access_token(user_name=login_request.user_name)
    return {"access_token": token, "token_type": "Bearer"}


@router.get("")
async def get_user(user: dict = Depends(get_current_user)):
    return user
