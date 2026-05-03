from typing import List
from datetime import datetime
from pydantic import BaseModel

class ScrapeOpenCnpjRequest(BaseModel):
    cnpj_list: List[str]

class ScrapeOpenCnpjResponse(BaseModel):
    total_valid: int
    estimated_finish_time: datetime