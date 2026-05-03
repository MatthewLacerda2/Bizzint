import uuid
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.database import get_db
from ...schemas.shared_chat import (
    CreateSharedChatRequest,
    CreateSharedChatResponse,
    GetSharedChatResponse,
    SharedChatSchema
)
from ...repositories.shared_chat_repository import SharedChatRepository

router = APIRouter()

@router.post("/", response_model=CreateSharedChatResponse)
async def create_shared_chat(request: CreateSharedChatRequest, db: AsyncSession = Depends(get_db)):
    chat_id = uuid.uuid4()
    
    messages = request.messages
    db_objs = []
    
    i = 0
    order = 0
    while i < len(messages):
        if messages[i].role == "user":
            user_msg = messages[i].content
            assistant_msg = None
            plots = None
            
            if i + 1 < len(messages) and messages[i + 1].role == "assistant":
                assistant_msg = messages[i + 1].content
                if messages[i + 1].plots:
                    plots = [p.model_dump() for p in messages[i + 1].plots]
                i += 2
            else:
                i += 1
                
            db_objs.append({
                "chat_id": chat_id,
                "order": order,
                "user_message": user_msg,
                "assistant_message": assistant_msg,
                "plots": plots
            })
            order += 1
        else:
            assistant_msg = messages[i].content
            plots = None
            if messages[i].plots:
                plots = [p.model_dump() for p in messages[i].plots]
            
            db_objs.append({
                "chat_id": chat_id,
                "order": order,
                "user_message": "",
                "assistant_message": assistant_msg,
                "plots": plots
            })
            i += 1
            order += 1

    if not db_objs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No messages provided")

    repo = SharedChatRepository(db)
    created_chats = await repo.create_many(db_objs)
    
    return CreateSharedChatResponse(
        chat_id=chat_id,
        created_at=datetime.now()
    )

@router.get("/{chat_id}", response_model=GetSharedChatResponse)
async def get_shared_chat(chat_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    repo = SharedChatRepository(db)
    shared_chats = await repo.get_by_chat_id(chat_id)
    
    if not shared_chats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shared chat not found")
        
    messages_out = []
    for chat in shared_chats:
        plots = chat.plots if chat.plots else None
        
        messages_out.append(
            SharedChatSchema(
                order=chat.order,
                user_message=chat.user_message,
                assistant_message=chat.assistant_message,
                plots=plots
            )
        )
        
    return GetSharedChatResponse(messages=messages_out)