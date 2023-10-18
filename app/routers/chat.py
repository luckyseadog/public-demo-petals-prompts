from typing import Dict

from fastapi import APIRouter

from model.model import NeuralNetworkModel
from database.database import SQLDatabase


model = NeuralNetworkModel("petals-team/StableBeluga2")

db = SQLDatabase("messages.db")

router = APIRouter()

@router.get("/chat")
def get_messages():
    db.execute("SELECT * FROM messages ORDER BY date DESC LIMIT 7")
    messages = db.fetchall()
    messages = [
        {"id": m[0], "user": m[1], "date": m[2], "content": m[3]} for m in messages
    ]
    messages.reverse()
    return messages


@router.post("/chat/add_message")
def add_message(data: Dict[str, str]):
    ai_tokens = model.inference(data["content"])
    ai_message = "".join(ai_tokens)
    db.execute(
        'INSERT INTO messages (user, date, content) VALUES (?, datetime("now", "localtime"), ?)',
        ("AI", ai_message),
    )
    db.execute(
        'INSERT INTO messages (user, date, content) VALUES (?, datetime("now", "localtime"), ?)',
        ("Human", data["content"]),
    )
    db.commit()
