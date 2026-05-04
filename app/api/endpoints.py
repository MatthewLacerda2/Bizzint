from fastapi import APIRouter
from .v1 import chatbot, opencnpj, shared_chat, gen_report

router = APIRouter()

router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
router.include_router(opencnpj.router, prefix="/opencnpj", tags=["opencnpj"])
router.include_router(shared_chat.router, prefix="/shared-chat", tags=["shared-chat"])
router.include_router(gen_report.router, prefix="/gen-report", tags=["report"])