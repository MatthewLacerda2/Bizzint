from pydantic import BaseModel

class ChatbotRequest(BaseModel):
    prompt: str

class ChatbotResponse(BaseModel):
    response: str