import logging as logger
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.chat import ConnectionManager


router = APIRouter()


class ChatController:
    """
    Websocket endpoint for chatting
    """

    @staticmethod
    @router.websocket("/")
    async def websocket_endpoint(websocket: WebSocket):
        manager = ConnectionManager()
        await manager.connect(websocket)
        logger.info("Connected")

        try:
            while True:
                data = await websocket.receive_text()
                await manager.broadcast({"data": data})
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            logger.info("Disconnected")
