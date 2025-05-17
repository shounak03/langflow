from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
)
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from ...database.session import get_db
from ...database.models import ChatMessage
from typing import List
from datetime import datetime

load_dotenv()
OPENAI_API_KEY = os.getenv("API_KEY")

router = APIRouter(tags=["chat_gpt"])

class PromptRequest(BaseModel):
    prompt: str

class ChatMessageResponse(BaseModel):
    id: int
    prompt: str
    response: str
    timestamp: datetime

    class Config:
        from_attributes = True

@router.post("/chat_gpt")
async def chat_gpt(request: PromptRequest, db: Session = Depends(get_db)):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="API Key not set")
    
    try:
        chat = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            temperature=0,
        )
        message = HumanMessage(content=request.prompt)
        resp = chat([message]).content
        
        # Store in database
        chat_message = ChatMessage(
            prompt=request.prompt,
            response=resp
        )
        db.add(chat_message)
        db.commit()
        
        return {"response": resp}
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat_history")
async def get_chat_history(db: Session = Depends(get_db)):
    try:
        # Get all messages ordered by timestamp
        messages = db.query(ChatMessage).order_by(ChatMessage.timestamp.desc()).all()
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat_gpt_check")
async def check():
    return {"message": "chat gpt route check"}
