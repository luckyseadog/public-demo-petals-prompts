import asyncio
from typing import Dict
import websockets

from fastapi import APIRouter, Query, WebSocket

from app.model.model import NeuralNetworkModel

# from database.database import SQLDatabase
from app.settings.config import Config
from app.storage.sqlite import SqliteConnector

model = NeuralNetworkModel("petals-team/StableBeluga2")
config = Config.load()
db = SqliteConnector(config.storage)

router = APIRouter()


@router.get("/chat")
def get_messages(chat_id=Query(0)):
    messages = db.select_by_chat(chat_id=chat_id, limit=7)
    messages = [
        {"message_id": m[0], "chat_id": m[1], "date": m[2], "is_ai": m[3], "content": m[4]}
        for m in messages
    ]
    messages.reverse()
    return messages

async def send_and_return(message_deq, result, websocket):
     while True:
        message = await message_deq.get()
        await result.put(message)
        await websocket.send_text(message)
        message_deq.task_done()
     

@router.websocket("/chat/add-massage-websocket")
async def receiver(data: Dict[str, str], websocket: WebSocket):
    db.insert(chat_id=data["chat_id"], is_ai=False, content=data["content"])
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        message_deq = asyncio.Queue()
        result_deq = asyncio.Queue()
        
        producer = asyncio.create_task(model.inference_websocket(data["content"], message_deq, plug=False))
        consumer = asyncio.create_task(send_and_return(message_deq, result_deq, websocket))

        await asyncio.gather(producer)
        await message_deq.join()
        consumer.cancel()

        ai_message = None
        while not result_deq.empty():
            ai_message = await result_deq.get()

        db.insert(chat_id=data["chat_id"], is_ai=True, content=ai_message)


@router.post("/chat/add_message")
def add_message(data: Dict[str, str]):
    db.insert(chat_id=data["chat_id"], is_ai=False, content=data["content"])
    ai_tokens = model.inference(data["content"], plug=False)
    ai_message = "".join(ai_tokens)
    db.insert(chat_id=data["chat_id"], is_ai=True, content=ai_message)
