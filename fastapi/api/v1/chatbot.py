from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def chat():
    return {"message": "Chatbot is working"}
