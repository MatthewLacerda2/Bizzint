from pydantic import BaseModel
from typing import List
from .chatbot import ChatMessage

class GenerateReportRequest(BaseModel):
    commentary: str
    messages: List[ChatMessage]

class GenerateReportResponse(BaseModel):
    report: bytes