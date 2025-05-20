from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn

SQLALCHEMY_DATABASE_URL = "sqlite:///./messages.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    class Config:
        orm_mode = True

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
async def get_messages(db: Session = Depends(get_db)):
    messages = db.query(MessageModel).all()
    return messages


@app.post("/api/messages", response_model=Message, status_code=201)
async def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    db_message = db.query(MessageModel).filter(MessageModel.text == message.text).first()
    if db_message:
        raise HTTPException(status_code=400, detail=f"Message with text \"{message.text}\" already exists")
    new_message = MessageModel(text=message.text)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
