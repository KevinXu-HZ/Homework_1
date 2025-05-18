from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Message(BaseModel):
    id: int
    text: str

class MessageCreate(BaseModel):
    text: str

messages_db = [
    Message(id=1, text="Hello from FastAPI!"),
    Message(id=2, text="This is a demo message")
]

@app.get("/")
async def root():
    return {"status": "ok", "message": "FastAPI server is running"}

@app.get("/api/messages", response_model=List[Message])
async def get_messages():
    return messages_db

@app.post("/api/messages", response_model=Message, status_code=201)
async def create_message(message: MessageCreate):
    if any (m.text == message.text for m in messages_db):
        raise HTTPException(status_code=400, detail=f"Message with text \"{message.text}\" already exists")
    else:
        new_id = max([m.id for m in messages_db], default=0) + 1
        new_message = Message(id=new_id, text=message.text)
        messages_db.append(new_message)
        return new_message

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)