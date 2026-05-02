from typing import List
from datetime import datetime
from pydantic import BaseModel

class ScrapeOpenCnpjRequest(BaseModel):
    cnpj_list: List[str]

class ScrapeOpenCnpjResponse(BaseModel):
    valid_cnpj_list: List[str]
    total_invalid: int
    total_duplicated: int
    total_received: int
    total_valid: int
    estimated_finish_time: datetime