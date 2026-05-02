from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import BaseRepository
from ..models.company import Company

class CompanyRepository(BaseRepository[Company]):
    def __init__(self, db: AsyncSession):
        super().__init__(Company, db)

    async def get_by_cnpj(self, cnpj: str) -> Optional[Company]:
        """
        Fetch a company by its CNPJ.
        """
        query = select(self.model).where(self.model.cnpj == cnpj)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()