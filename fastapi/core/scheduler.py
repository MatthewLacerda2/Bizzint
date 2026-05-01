import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
#from whatever_file import whatever_function

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

def setup_scheduler_jobs() -> None:

    print("hello world")

    #scheduler.add_job(
    #    whatever_function,
    #    trigger=CronTrigger(hour=0, minute=5),
    #    id="whatever_id",
    #    name="Whatever Name",
    #    replace_existing=True,
    #    max_instances=1  # Ensure only one instance runs at a time
    #)

def start_scheduler() -> None:
    """Start the scheduler."""
    logger.info("Starting APScheduler")
    scheduler.start()
    logger.info("Scheduler started")


def stop_scheduler() -> None:
    """Stop the scheduler."""
    scheduler.shutdown()