import uvicorn
from fastapi import FastAPI
from app.api.api_v1 import api_v1

app = FastAPI(title="Chat Application")

app.include_router(api_v1, prefix="/api/v1")


# Root endpoint for health check
@app.get("/")
async def root():
    return {"message": "Chat app is running!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
