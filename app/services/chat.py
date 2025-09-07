import asyncio
import json
import logging
from fastapi import WebSocket
from websockets import ConnectionClosedError
from typing import List, Union
from app.core.redis_manager import get_redis_client
from redis.asyncio import Redis

__all__ = ["ChatService", "init_chat_service", "get_chat_service"]

logger = logging.getLogger(__name__)
CHATROOM_CHANNEL = "CHATROOM"


class ChatService:
    def __init__(self, redis_client: Redis):
        self.active_connections: List[WebSocket] = []
        self.pubsub_client = redis_client.pubsub()
        self.redis_client = redis_client

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(
            f"New connection started, Total active connections {len(self.active_connections)}"
        )

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(
                f"Client disconnected, Total active connections {len(self.active_connections)}"
            )

    async def broadcast_to_local_clients(self, message: str):
        message = {"data": message}
        message = json.dumps(message)
        dead_connections = []
        # Iterate over a copy of the list to safely modify the original.
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except (ConnectionClosedError, RuntimeError) as e:
                # RuntimeError can occur if the connection is in a closing state.
                logger.warning(f"Removing dead connection: {e}")
                dead_connections.append(connection)

        # Remove all dead connections found during the broadcast.
        for dead in dead_connections:
            await self.disconnect(dead)

    async def publish_to_redis(self, message: dict):
        message = json.dumps(message)
        await self.redis_client.publish(channel=CHATROOM_CHANNEL, message=message)

    async def pubsub_listener(self):
        await self.pubsub_client.subscribe(CHATROOM_CHANNEL)
        logger.info(f"Subscribed to channel {CHATROOM_CHANNEL}")
        try:
            while True:
                message = await self.pubsub_client.get_message(
                    ignore_subscribe_messages=True
                )
                if message and message["type"] == "message":
                    data: str = message["data"]
                    logger.debug(f"Received message from redis: {data}")
                    await self.broadcast_to_local_clients(data)

        except Exception as e:
            logger.error(f"Redis pub/sub lister error {e}")

        finally:
            await self.pubsub_client.unsubscribe(CHATROOM_CHANNEL)
            logger.info("Unsubscribed from Redis channel")


chat_service: Union[ChatService, None] = None


async def init_chat_service():
    """
    Initializes the chat service singleton after Redis is ready and starts the listener.
    """
    global chat_service
    redis_client = await get_redis_client()
    chat_service = ChatService(redis_client=redis_client)
    asyncio.create_task(chat_service.pubsub_listener())


async def get_chat_service() -> ChatService:
    """
    Dependency function to get the chat service instance.
    Ensures that the service is not used before it is initialized.
    """
    if chat_service is None:
        raise RuntimeError("Chat service is not initialized.")
    return chat_service
