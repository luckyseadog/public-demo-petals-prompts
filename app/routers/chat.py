from typing import Dict

from fastapi import APIRouter

from model.model import NeuralNetworkModel
from database.database import SQLDatabase


model = NeuralNetworkModel("petals-team/StableBeluga2")

db = SQLDatabase("messages.db")
db.create_table()

router = APIRouter()

@router.get("/chat")
def get_messages():
    messages = db.select_all(limit=7)
    messages = [
        {"messege_id": m[0], "chat_id": m[1], "date": m[2], "AI":m[3], "content": m[4]} for m in messages
    ]
    messages.reverse()
    return messages


@router.post("/chat/add_message")
def add_message(data: Dict[str, str]):
    db.add_record(values=(False, data["content"]))
    ai_tokens = model.inference(data["content"], plug=True)
    ai_message = "".join(ai_tokens)
    db.add_record(values=(True, ai_message))
