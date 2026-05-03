import httpx
import logging
import os
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ...repositories.whatsapp_number_repository import WhatsappNumberRepository

logger = logging.getLogger(__name__)

import re

WHATS_SERVICE_URL = os.getenv("WHATS_SERVICE_URL", "http://whatsservice:3000")

def is_valid_phone(phone: str) -> bool:
    clean_phone = re.sub(r"\D", "", phone)
    return 10 <= len(clean_phone) <= 13

async def validate_and_save_numbers(phone_numbers: List[str], db: AsyncSession):
    """
    Send numbers to whatsservice Go microservice and save/update results in DB.
    """
    if not phone_numbers:
        return

    # Filter invalid numbers
    valid_numbers = [n for n in phone_numbers if is_valid_phone(n)]
    invalid_numbers = [n for n in phone_numbers if not is_valid_phone(n)]
    
    if invalid_numbers:
        print(f"DEBUG: Filtered out invalid numbers: {invalid_numbers}")
    
    print(f"DEBUG: Validating numbers: {valid_numbers}")

    if not valid_numbers:
        return

    whats_repo = WhatsappNumberRepository(db)
    url = f"{WHATS_SERVICE_URL}/validate-bunch"

    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Sending {len(valid_numbers)} numbers to validation service")
            response = await client.post(url, json={"numbers": valid_numbers}, timeout=60.0)
            response.raise_for_status()
            
            data = response.json()
            results = data.get("phone_numbers", [])
            
            for item in results:
                phone = item["phone"]
                wa_data = {
                    "phone_number": phone,
                    "is_on_whatsapp": item["is_os_whatsapp_"],
                    "is_business": item["is_business"]
                }
                
                existing = await whats_repo.get_by_phone(phone)
                if existing:
                    await whats_repo.update(existing.id, wa_data)
                else:
                    await whats_repo.create(wa_data)
                    
            logger.info(f"Successfully processed and saved {len(results)} WhatsApp numbers")
            
    except httpx.HTTPError as e:
        logger.error(f"Error communicating with whatsservice: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in validate_and_save_numbers: {e}")
        raise