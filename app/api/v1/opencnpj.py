import re
from datetime import datetime, timedelta
from typing import List, Set
from fastapi import APIRouter
from ...schemas.opencnpj import ScrapeOpenCnpjRequest, ScrapeOpenCnpjResponse
from ...utils.cnpj_validation import validate_cnpj
from ...utils.envs import OPENCNPJ_DELAY
from ...services.cronjobs.opencnpj.fetcher import add_cnpjs_to_queue, cnpj_queue

router = APIRouter()

@router.post("/", response_model=ScrapeOpenCnpjResponse)
async def cnpj_search(request: ScrapeOpenCnpjRequest):
    total_received = len(request.cnpj_list)
    
    seen_cnpjs: Set[str] = set()
    valid_cnpj_list: List[str] = []
    
    total_invalid = 0
    total_duplicated = 0
    
    for raw_cnpj in request.cnpj_list:
        try:
            cleaned = validate_cnpj(raw_cnpj)
            
            if cleaned in seen_cnpjs:
                total_duplicated += 1
                continue
                
            seen_cnpjs.add(cleaned)
            valid_cnpj_list.append(cleaned)
        except ValueError:
            total_invalid += 1
            continue
    
    total_valid = len(valid_cnpj_list)
    
    # Start the scraping in the background via queue
    await add_cnpjs_to_queue(valid_cnpj_list)
    
    current_queue_size = cnpj_queue.qsize() if cnpj_queue else len(valid_cnpj_list)
    estimated_finish_time = datetime.now() + timedelta(seconds=current_queue_size * OPENCNPJ_DELAY)
    
    return ScrapeOpenCnpjResponse(
        total_valid=total_valid,
        estimated_finish_time=estimated_finish_time
    )