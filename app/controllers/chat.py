from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.services.chat import ChatService, get_chat_service
from app.types.chat_types import ChatInput


router = APIRouter()


class ChatController:
    """
    Websocket endpoint for chatting
    """

    @staticmethod
    @router.websocket("/")
    async def websocket_endpoint(
        websocket: WebSocket,
        chat_service_instance: ChatService = Depends(get_chat_service),
    ):
        await chat_service_instance.connect(websocket)
        try:
            while True:
                data: ChatInput = await websocket.receive_json()
                await chat_service_instance.publish_to_redis(data)

        except WebSocketDisconnect:
            await chat_service_instance.disconnect(websocket)
