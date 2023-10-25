from typing import Dict

from fastapi import APIRouter

from app.model.model import NeuralNetworkModel

# from database.database import SQLDatabase
from app.settings.config import Config
from app.storage.sqlite import SqliteConnector

model = NeuralNetworkModel("petals-team/StableBeluga2")
config = Config.load("config.yaml")
db = SqliteConnector(config.storage)

router = APIRouter()


@router.get("/chat")
def get_messages():
    messages = db.select_all(limit=20)
    messages = [
        {"message_id": m[0], "chat_id": m[1], "date": m[2], "is_ai": m[3], "content": m[4]}
        for m in messages
    ]
    messages.reverse()
    return messages


@router.post("/chat/add_message")
def add_message(data: Dict[str, str]):
    db.insert(values=(False, data["content"]))
    ai_tokens = model.inference(data["content"], plug=False)
    ai_message = "".join(ai_tokens)
    db.insert(values=(True, ai_message))
