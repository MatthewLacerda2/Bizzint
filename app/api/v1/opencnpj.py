import re
from datetime import datetime, timedelta
from typing import List, Set
from fastapi import APIRouter, BackgroundTasks
from ...schemas.opencnpj import ScrapeOpenCnpjRequest, ScrapeOpenCnpjResponse
from ...utils.envs import OPENCNPJ_DELAY
from ...services.cronjobs.opencnpj.fetcher import fetch_and_save_cnpjs

router = APIRouter()

def is_valid_cnpj_format(cnpj: str) -> bool:
    pattern = r'^(\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}|\d{14})$'
    return bool(re.match(pattern, cnpj))

def clean_cnpj(cnpj: str) -> str:
    return re.sub(r'\D', '', cnpj)

@router.post("/", response_model=ScrapeOpenCnpjResponse)
async def cnpj_search(request: ScrapeOpenCnpjRequest, background_tasks: BackgroundTasks):
    total_received = len(request.cnpj_list)
    
    seen_cnpjs: Set[str] = set()
    valid_cnpj_list: List[str] = []
    
    total_invalid = 0
    total_duplicated = 0
    
    for raw_cnpj in request.cnpj_list:
        if not is_valid_cnpj_format(raw_cnpj):
            total_invalid += 1
            continue
        
        cleaned = clean_cnpj(raw_cnpj)
        
        if cleaned in seen_cnpjs:
            total_duplicated += 1
            continue
            
        seen_cnpjs.add(cleaned)
        valid_cnpj_list.append(cleaned)
    
    total_valid = len(valid_cnpj_list)
    
    estimated_finish_time = datetime.now() + timedelta(seconds=total_valid * OPENCNPJ_DELAY)

    # Start the scraping in the background
    background_tasks.add_task(fetch_and_save_cnpjs, valid_cnpj_list)
    
    return ScrapeOpenCnpjResponse(
        valid_cnpj_list=valid_cnpj_list,
        total_invalid=total_invalid,
        total_duplicated=total_duplicated,
        total_received=total_received,
        total_valid=total_valid,
        estimated_finish_time=estimated_finish_time
    )