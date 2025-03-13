from fastapi import APIRouter
from app.services.services.smoke import SmokeService
router = APIRouter()


class SmokeController:
    @staticmethod
    @router.get('/')
    async def get():
        response = await SmokeService.get_version()
        return response
