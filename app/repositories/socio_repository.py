from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import BaseRepository
from ..models.socio import Socio

class SocioRepository(BaseRepository[Socio]):
    def __init__(self, db: AsyncSession):
        super().__init__(Socio, db)

    async def get_by_company_id(self, company_id: str) -> List[Socio]:
        """
        Fetch all partners associated with a specific company ID.
        """
        query = select(self.model).where(self.model.company_id == company_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())
