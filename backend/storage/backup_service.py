import shutil
import os
import sqlite3
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_FILE = "storage/app.db"
BACKUP_DB_FILE = "storage/app_backup.db"
BACKUP_FOLDER = "storage/backups"

def ensure_backup_folder():
    """Create backup folder if it doesn't exist"""
    Path(BACKUP_FOLDER).mkdir(parents=True, exist_ok=True)

def create_backup_database():
    """Initialize backup database with same schema as main database"""
    try:
        # Check if main database exists
        if not os.path.exists(DB_FILE):
            logger.warning(f"Main database {DB_FILE} does not exist yet")
            return False
        
        # Create backup database directory if needed
        os.makedirs(os.path.dirname(BACKUP_DB_FILE), exist_ok=True)
        
        # If backup doesn't exist, copy the main database
        if not os.path.exists(BACKUP_DB_FILE):
            shutil.copy2(DB_FILE, BACKUP_DB_FILE)
            logger.info(f"Backup database created at {BACKUP_DB_FILE}")
        
        return True
    except Exception as e:
        logger.error(f"Error creating backup database: {str(e)}")
        return False

def backup_to_secondary_db():
    """Backup main database to secondary backup database"""
    try:
        if not os.path.exists(DB_FILE):
            logger.warning(f"Main database {DB_FILE} does not exist")
            return False
        
        # Create backup database if it doesn't exist
        create_backup_database()
        
        # Copy main database to backup
        shutil.copy2(DB_FILE, BACKUP_DB_FILE)
        logger.info(f"Database backed up to {BACKUP_DB_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error backing up to secondary database: {str(e)}")
        return False

def backup_to_timestamped_file():
    """Create a timestamped backup file in backups folder"""
    try:
        ensure_backup_folder()
        
        if not os.path.exists(DB_FILE):
            logger.warning(f"Main database {DB_FILE} does not exist")
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_FOLDER, f"app_backup_{timestamp}.db")
        
        shutil.copy2(DB_FILE, backup_file)
        logger.info(f"Timestamped backup created: {backup_file}")
        
        # Clean up old backups (keep last 50)
        cleanup_old_backups(keep_count=50)
        
        return True
    except Exception as e:
        logger.error(f"Error creating timestamped backup: {str(e)}")
        return False

def cleanup_old_backups(keep_count: int = 50):
    """Remove old backup files, keeping only the most recent ones"""
    try:
        ensure_backup_folder()
        backup_files = sorted(
            Path(BACKUP_FOLDER).glob("app_backup_*.db"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        # Remove old backups beyond keep_count
        for old_backup in backup_files[keep_count:]:
            old_backup.unlink()
            logger.info(f"Removed old backup: {old_backup}")
    except Exception as e:
        logger.error(f"Error cleaning up old backups: {str(e)}")

def restore_from_backup():
    """Restore main database from backup database"""
    try:
        if not os.path.exists(BACKUP_DB_FILE):
            logger.error(f"Backup database {BACKUP_DB_FILE} does not exist")
            return False
        
        # Create a safety backup before restoring
        if os.path.exists(DB_FILE):
            safety_backup = f"{DB_FILE}.before_restore"
            shutil.copy2(DB_FILE, safety_backup)
            logger.info(f"Safety backup created at {safety_backup}")
        
        # Restore from backup
        shutil.copy2(BACKUP_DB_FILE, DB_FILE)
        logger.info(f"Database restored from {BACKUP_DB_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error restoring from backup: {str(e)}")
        return False

def verify_database_integrity(db_path: str) -> bool:
    """Verify SQLite database integrity"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        conn.close()
        
        is_valid = result[0] == "ok"
        if is_valid:
            logger.info(f"Database {db_path} integrity check passed")
        else:
            logger.error(f"Database {db_path} integrity check failed: {result[0]}")
        
        return is_valid
    except Exception as e:
        logger.error(f"Error verifying database integrity: {str(e)}")
        return False

def get_backup_info():
    """Get information about backups"""
    info = {
        "main_db_exists": os.path.exists(DB_FILE),
        "backup_db_exists": os.path.exists(BACKUP_DB_FILE),
        "main_db_size": os.path.getsize(DB_FILE) if os.path.exists(DB_FILE) else 0,
        "backup_db_size": os.path.getsize(BACKUP_DB_FILE) if os.path.exists(BACKUP_DB_FILE) else 0,
        "timestamped_backups": len(list(Path(BACKUP_FOLDER).glob("app_backup_*.db"))) if os.path.exists(BACKUP_FOLDER) else 0
    }
    
    if info["main_db_exists"]:
        info["main_db_modified"] = datetime.fromtimestamp(
            os.path.getmtime(DB_FILE)
        ).isoformat()
    
    if info["backup_db_exists"]:
        info["backup_db_modified"] = datetime.fromtimestamp(
            os.path.getmtime(BACKUP_DB_FILE)
        ).isoformat()
    
    return info