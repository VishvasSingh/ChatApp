import pydantic
from fastapi import APIRouter, HTTPException, Request, Depends
from app.auth.jwt_handler import create_access_token
from app.auth.dependencies import get_current_user
from app.schemas.login import LoginRequest

router = APIRouter()


@router.post("")
async def login(request: Request):
    request_body = await request.json()
    try:
        request_body_schema = LoginRequest(**request_body)

    except pydantic.ValidationError:
        raise HTTPException(status_code=404, detail="Request body schema is invalid")

    token = create_access_token(user_name=request_body_schema.user_name)
    return {"access_token": token, "token_type": "Bearer"}


@router.get("")
async def get_user(user: dict = Depends(get_current_user)):
    return user
