import json

from fastapi import FastAPI, WebSocket
from typing import List
from datetime import datetime

app = FastAPI()

# Connection manager to handle WebSocket connections


class ConnectionManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._active_connections = list()

        return cls._instance

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self._active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self._active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict):
        message = json.dumps(message)
        for connection in self._active_connections:
            await connection.send_text(message)
        self.save_message(message)

    def save_message(self, message: str):
        with open("chat_history.txt", "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{timestamp}] {message}\n")
