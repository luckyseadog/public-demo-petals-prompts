from typing import Dict

from fastapi import APIRouter
import sqlite3

from transformers import AutoTokenizer
from petals import AutoDistributedModelForCausalLM

model_name = "petals-team/StableBeluga2"

tokenizer = AutoTokenizer.from_pretrained(
    model_name, use_fast=False, add_bos_token=False
)
model = AutoDistributedModelForCausalLM.from_pretrained(model_name)
fake_token = tokenizer("^")["input_ids"][0]


conn = sqlite3.connect("messages.db", check_same_thread=False)

cur = conn.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS messages(
   id INTEGER PRIMARY KEY,
   user VARCHAR(32),
   date DATETIME,
   content TEXT);
"""
)


router = APIRouter()


cur.execute(
    """CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    user VARCHAR(32),
    date DATETIME,
    content TEXT
);"""
)


@router.get("/chat")
def get_messages():
    cur.execute("SELECT * FROM messages ORDER BY date DESC LIMIT 7")
    messages = cur.fetchall()
    messages = [
        {"id": m[0], "user": m[1], "date": m[2], "content": m[3]} for m in messages
    ]
    messages.reverse()
    return messages


@router.post("/chat/add_message")
def add_message(data: Dict[str, str]):
    with model.inference_session(max_length=512) as sess:
        prompt = data["content"]
        print(prompt)
        prefix = f"Human: {prompt}\nFriendly AI:"
        prefix = tokenizer(prefix, return_tensors="pt")["input_ids"]
        ai_tokens = []
        while True:
            outputs = model.generate(
                prefix,
                max_new_tokens=1,
                session=sess,
                do_sample=True,
                temperature=0.9,
                top_p=0.6,
            )
            outputs = tokenizer.decode([fake_token, outputs[0, -1].item()])[1:]
            ai_tokens.append(outputs)

            if "\n" in outputs or "</s>" in outputs:
                break
            prefix = (
                None  # Prefix is passed only for the 1st token of the bot's response
            )
    ai_message = "".join(ai_tokens)
    cur.execute(
        'INSERT INTO messages (user, date, content) VALUES (?, datetime("now", "localtime"), ?)',
        ("AI", ai_message),
    )
    cur.execute(
        'INSERT INTO messages (user, date, content) VALUES (?, datetime("now", "localtime"), ?)',
        ("Human", data["content"]),
    )
    conn.commit()
