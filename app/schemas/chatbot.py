from pydantic import BaseModel
from typing import Any, Literal, Optional, List, Dict

class PlotData(BaseModel):
    """
    Structured data for rendering charts in the frontend.
    """
    data: List[Dict[str, Any]]
    chart_type: Literal["line", "bar", "pie"]
    title: Optional[str] = None
    description: Optional[str] = None

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    plots: Optional[List[PlotData]] = None

class ChatbotRequest(BaseModel):
    prompt: str
    history: List[ChatMessage] = []

class ChatStreamEvent(BaseModel):
    """
    Represents a single event in the chatbot's streaming response.
    Used for NDJSON streaming to the frontend.
    """
    type: Literal["text", "plot", "error"]
    content: Optional[str] = None
    plot: Optional[PlotData] = None