from fastapi import APIRouter
from .v1 import chatbot, opencnpj

router = APIRouter()

router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
router.include_router(opencnpj.router, prefix="/opencnpj", tags=["opencnpj"])