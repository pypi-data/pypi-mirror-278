import sqlite3
from fastapi import FastAPI, Depends, HTTPException,Request
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Create users database and table
user_conn = sqlite3.connect('user_database.db')
user_cursor = user_conn.cursor()

user_cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    fullname TEXT NOT NULL
)
''')

user_conn.commit()

# Create chat history database and tables
chat_conn = sqlite3.connect('chat_history.db')
chat_cursor = chat_conn.cursor()

chat_cursor.execute('''
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

chat_cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER,
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(conversation_id) REFERENCES conversations(id)
)
''')

chat_conn.commit()

# Dependency to establish user database connection
def get_user_db_conn():
    user_conn = sqlite3.connect('user_database.db')
    return user_conn

# Dependency to establish chat history database connection
def get_chat_db_conn():
    chat_conn = sqlite3.connect('chat_history.db')
    return chat_conn

# Models
class User(BaseModel):
    username: str
    password: str
    fullname: str

class Conversation(BaseModel):
    user_id: int

class Message(BaseModel):
    message: str

# Routes
@app.post("/signup/")
async def user_signup(user: User, db_conn = Depends(get_user_db_conn)):
    cursor = db_conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password, fullname) VALUES (?, ?, ?)', (user.username, user.password, user.fullname))
        db_conn.commit()
        return {"message": "User signed up successfully!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already taken")

@app.post("/login/")
async def user_login(user: User, db_conn = Depends(get_user_db_conn)):
    cursor = db_conn.cursor()
    cursor.execute('SELECT id, fullname FROM users WHERE username = ? AND password = ?', (user.username, user.password))
    user_info = cursor.fetchone()
    if user_info:
        user_id = user_info[0]
        fullname = user_info[1]
        return {"message": f"Welcome, {fullname}!", "user_id": user_id}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.post("/conversations/")
async def start_conversation(conversation: Conversation, db_conn = Depends(get_chat_db_conn)):
    cursor = db_conn.cursor()
    cursor.execute('INSERT INTO conversations (user_id) VALUES (?)', (conversation.user_id,))
    db_conn.commit()
    conversation_id = cursor.lastrowid
    return {"message": "Conversation started successfully!", "conversation_id": conversation_id}

@app.post("/conversations/{conversation_id}/messages/")
async def add_message(conversation_id: int, message: Message, db_conn = Depends(get_chat_db_conn)):
    cursor = db_conn.cursor()
    cursor.execute('INSERT INTO messages (conversation_id, message) VALUES (?, ?)', (conversation_id, message.message))
    db_conn.commit()
    return {"message": "Message added successfully!"}

@app.get("/conversations/")
async def fetch_conversations(user_id: int, db_conn = Depends(get_chat_db_conn)):
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM conversations WHERE user_id = ?', (user_id,))
    conversations = cursor.fetchall()
    return conversations

@app.get("/conversations/{conversation_id}/")
async def fetch_conversation_by_id(conversation_id: int, user_id: int, db_conn = Depends(get_chat_db_conn)):
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM conversations WHERE id = ? AND user_id = ?', (conversation_id, user_id))
    conversation = cursor.fetchone()
    if conversation:
        cursor.execute('SELECT message FROM messages WHERE conversation_id = ?', (conversation_id,))
        messages = cursor.fetchall()
        return {"conversation": conversation, "messages": messages}
    else:
        raise HTTPException(status_code=404, detail="Conversation not found")

# Dependency to close user database connection after request
@app.middleware("http")
async def close_user_db_connection(request: Request, call_next):
    response = await call_next(request)
    user_conn.close()
    return response

# Dependency to close chat history database connection after request
@app.middleware("http")
async def close_chat_db_connection(request: Request, call_next):
    response = await call_next(request)
    chat_conn.close()
    return response
