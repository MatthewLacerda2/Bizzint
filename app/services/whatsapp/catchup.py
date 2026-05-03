import logging
from datetime import datetime
from sqlalchemy import select, and_, extract
from ...core.database import AsyncSessionLocal
from ...models.company import Company
from ...models.whatsapp_number import WhatsappNumber
from .validate_numbers import validate_and_save_numbers

logger = logging.getLogger(__name__)

async def run_whatsapp_catchup():
    """
    Scans all companies for phone numbers and validates those that haven't
    been updated in the current month.
    """
    logger.info("Starting WhatsApp catch-up task...")
    
    async with AsyncSessionLocal() as db:
        try:
            # 1. Get all unique phones from Company table
            query = select(Company.telefone_1, Company.telefone_2)
            result = await db.execute(query)
            
            all_phones = set()
            for t1, t2 in result:
                if t1:
                    all_phones.add(t1)
                if t2:
                    all_phones.add(t2)
            
            if not all_phones:
                logger.info("No phone numbers found in companies table.")
                return

            # 2. Identify phones that were already updated this month
            now = datetime.now()
            query_existing = select(WhatsappNumber.phone_number).where(
                and_(
                    extract('month', WhatsappNumber.last_updated_at) == now.month,
                    extract('year', WhatsappNumber.last_updated_at) == now.year
                )
            )
            result_existing = await db.execute(query_existing)
            updated_this_month = {row[0] for row in result_existing.all()}

            # 3. Filter out numbers that are already up-to-date
            phones_to_validate = [p for p in all_phones if p not in updated_this_month]

            if not phones_to_validate:
                logger.info("All phone numbers are already updated for this month.")
                return

            logger.info(f"Catch-up: Found {len(phones_to_validate)} numbers to validate/update.")
            
            # 4. Run validation in batches (if necessary, though validate_and_save_numbers handles the call)
            # For catchup, we might want to do it in chunks if the list is massive
            chunk_size = 10000
            for i in range(0, len(phones_to_validate), chunk_size):
                chunk = phones_to_validate[i:i + chunk_size]
                logger.info(f"Processing catch-up chunk {i//chunk_size + 1} ({len(chunk)} numbers)")
                await validate_and_save_numbers(chunk, db)
                
            logger.info("WhatsApp catch-up task completed successfully.")
            
        except Exception as e:
            logger.error(f"Error during WhatsApp catch-up: {e}", exc_info=True)
