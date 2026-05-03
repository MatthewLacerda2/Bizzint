from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from .chatbot import ChatMessage, PlotData

class CreateSharedChatRequest(BaseModel):
    messages: List[ChatMessage]

class CreateSharedChatResponse(BaseModel):
    chat_id: UUID
    created_at: datetime

class SharedChatSchema(BaseModel):
    order: int
    user_message: str
    assistant_message: Optional[str] = None
    plots: Optional[List[PlotData]] = None

class GetSharedChatResponse(BaseModel):
    messages: List[SharedChatSchema]