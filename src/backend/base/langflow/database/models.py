from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import os

Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String)
    response = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
os.makedirs(db_dir, exist_ok=True)


DATABASE_URL = f"sqlite:///{os.path.join(db_dir, 'chat_support_db.db')}"
engine = create_engine(DATABASE_URL) 