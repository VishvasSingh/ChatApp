import uvicorn
import logging.config
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.logging_config import LOGGING_CONFIG
from app.core.redis_manager import connect_to_redis, close_redis_connection
from app.services.chat import init_chat_service
from app.api.api_v1 import api_v1
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(application: FastAPI):
    await connect_to_redis()
    await init_chat_service()
    yield
    await close_redis_connection()


logging.config.dictConfig(LOGGING_CONFIG)
app = FastAPI(title="Chat Application", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your Angular app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1, prefix="/api/v1")
logger = logging.getLogger(__name__)
logger.info("App is now running")


# Root endpoint for health check
@app.get("/")
async def root():
    return {"message": "Chat app is running!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
