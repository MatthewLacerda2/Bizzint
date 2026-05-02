from fastapi import APIRouter
from .v1 import chatbot

router = APIRouter()

router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])