import asyncio
import logging
from contextlib import asynccontextmanager
from services.backup_service import backup_to_secondary_db, backup_to_timestamped_file, create_backup_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

backup_task = None

async def periodic_backup():
    logger.info("Starting periodic backup task (every 5 minutes)")
    
    create_backup_database()
    backup_to_secondary_db()
    
    while True:
        try:
            await asyncio.sleep(300)  # 5 minutes = 300 seconds
            
            logger.info("Running scheduled backup...")
            
            success = backup_to_secondary_db()
            
            backup_to_timestamped_file()
            
            if success:
                logger.info("Scheduled backup completed successfully")
            else:
                logger.error("Scheduled backup failed")
                
        except asyncio.CancelledError:
            logger.info("Backup task cancelled")
            break
        except Exception as e:
            logger.error(f"Error in periodic backup: {str(e)}")
            await asyncio.sleep(60)  # Wait a minute before retrying

@asynccontextmanager
async def lifespan_with_backup(app):
    global backup_task
    
    logger.info("Application starting up...")
    backup_task = asyncio.create_task(periodic_backup())
    
    yield
    
    logger.info("Application shutting down...")
    if backup_task:
        backup_task.cancel()
        try:
            await backup_task
        except asyncio.CancelledError:
            pass
    logger.info("Backup task stopped")