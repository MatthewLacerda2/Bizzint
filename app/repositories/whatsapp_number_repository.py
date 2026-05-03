from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import BaseRepository
from ..models.whatsapp_number import WhatsappNumber

class WhatsappNumberRepository(BaseRepository[WhatsappNumber]):
    def __init__(self, db: AsyncSession):
        super().__init__(WhatsappNumber, db)

    async def get_by_phone(self, phone_number: str) -> Optional[WhatsappNumber]:
        """
        Fetch a whatsapp number entry by the phone number string.
        """
        query = select(self.model).where(self.model.phone_number == phone_number)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()