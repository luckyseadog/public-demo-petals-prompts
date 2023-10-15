
from typing import Dict

from fastapi import APIRouter, HTTPException, Form
import sqlite3
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List

from fastapi.responses import RedirectResponse


conn = sqlite3.connect('messages.db', check_same_thread=False)

# Создаем курсор, специальный объект для взаимодействия с базой
cur = conn.cursor()

# Выполняем команду создания таблицы
cur.execute('''CREATE TABLE IF NOT EXISTS messages(
   id INTEGER PRIMARY KEY,
   user VARCHAR(32),
   date DATETIME,
   content TEXT);
''')




router = APIRouter()


# # Define a model for messages
# class Message(BaseModel):
#     user: str
#     content: str

cur.execute('''CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    user VARCHAR(32),
    date DATETIME,
    content TEXT
);''')

@router.get('/chat')
def get_messages():
    cur.execute('SELECT * FROM messages ORDER BY date DESC LIMIT 7')
    messages = cur.fetchall()
    messages = [{"id": m[0], "user": m[1], "date": m[2], "content": m[3]} for m in messages]
    messages.reverse()
    return messages

@router.post('/chat/add_message')
def add_message(data: Dict[str, str]):
    cur.execute('INSERT INTO messages (user, date, content) VALUES (?, datetime("now", "localtime"), ?)',
                ("AI", "Gamarjoba"))
    cur.execute('INSERT INTO messages (user, date, content) VALUES (?, datetime("now", "localtime"), ?)',
                ("Nikita", data['content']))
    conn.commit()
    # return RedirectResponse("http://localhost:8417/chat")
    
