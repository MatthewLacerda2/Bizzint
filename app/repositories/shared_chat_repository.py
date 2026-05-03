from typing import List, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseRepository
from ..models.shared_chat import SharedChat

class SharedChatRepository(BaseRepository[SharedChat]):
    def __init__(self, db: AsyncSession):
        super().__init__(SharedChat, db)

    async def get_by_chat_id(self, chat_id: Any) -> List[SharedChat]:
        """
        Returns all messages for a specific shared chat, 
        ordered by: order -> created_at -> id.
        """
        query = (
            select(self.model)
            .where(self.model.chat_id == chat_id)
            .order_by(
                self.model.order.asc(),
                self.model.created_at.asc(),
                self.model.id.asc()
            )
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create_many(self, obj_in_list: List[dict]) -> List[SharedChat]:
        db_objs = [self.model(**obj_in) for obj_in in obj_in_list]
        self.db.add_all(db_objs)
        await self.db.commit()
        return db_objs