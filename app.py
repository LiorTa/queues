from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from typing import Optional
import asyncio
import logging

app = FastAPI()

# Set up logging, will help us debug the system if something goes wrong
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Authentication setup, very very basic just for awareness
security = HTTPBasic()
AUTHORIZED_USERS = {"admin": "password123"}

# In-memory queue storage
QUEUES = {}


# Helper function: Authenticate users
def authenticate(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    if credentials.username not in AUTHORIZED_USERS or AUTHORIZED_USERS[credentials.username] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# POST: Add message to the queue
@app.post("/api/{queue_name}")
async def add_message(queue_name: str, request: Request, username: str = Depends(authenticate)) -> JSONResponse:
    print(request)
    logger.info(f"User '{username}' is adding a message to queue '{queue_name}'")
    if queue_name not in QUEUES:
        QUEUES[queue_name] = asyncio.Queue()
    message = await request.json()  # Parses JSON body
    await QUEUES[queue_name].put(message)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Message added to the queue"})


# GET: Retrieve message from the queue
@app.get("/api/{queue_name}")
async def get_message(queue_name: str, timeout: Optional[int] = 10000, username: str = Depends(authenticate)):
    print(queue_name)
    logger.info(f"User '{username}' is retrieving a message from queue '{queue_name}' with timeout {timeout}ms")
    if queue_name not in QUEUES or QUEUES[queue_name].empty():
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "No messages in the queue"})

    message = await asyncio.wait_for(QUEUES[queue_name].get(), timeout=timeout / 1000)
    return {"queue_name": queue_name, "messages": message}


# Server error handler
@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    logger.error(f"An error occurred: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred."},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)