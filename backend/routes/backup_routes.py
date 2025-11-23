from fastapi import APIRouter, HTTPException, status
from services.backup_service import (
    backup_to_secondary_db,
    backup_to_timestamped_file,
    restore_from_backup,
    verify_database_integrity,
    get_backup_info,
    DB_FILE,
    BACKUP_DB_FILE
)

router = APIRouter(prefix="/backup", tags=["Backup"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_backup():
    """Manually trigger a backup to the secondary database"""
    success = backup_to_secondary_db()
    if success:
        return {"message": "Backup created successfully", "backup_file": BACKUP_DB_FILE}
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to create backup"
        )

@router.post("/create-timestamped", status_code=status.HTTP_201_CREATED)
def create_timestamped_backup():
    """Create a timestamped backup file"""
    success = backup_to_timestamped_file()
    if success:
        return {"message": "Timestamped backup created successfully"}
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to create timestamped backup"
        )

@router.post("/restore", status_code=status.HTTP_200_OK)
def restore_backup():
    """Restore main database from backup database"""
    success = restore_from_backup()
    if success:
        return {"message": "Database restored from backup successfully"}
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to restore from backup"
        )

@router.get("/info")
def backup_information():
    """Get information about current backups"""
    return get_backup_info()

@router.get("/verify-main")
def verify_main_database():
    """Verify integrity of main database"""
    is_valid = verify_database_integrity(DB_FILE)
    if is_valid:
        return {"status": "valid", "database": "main", "message": "Database integrity check passed"}
    else:
        return {"status": "invalid", "database": "main", "message": "Database integrity check failed"}

@router.get("/verify-backup")
def verify_backup_database():
    """Verify integrity of backup database"""
    is_valid = verify_database_integrity(BACKUP_DB_FILE)
    if is_valid:
        return {"status": "valid", "database": "backup", "message": "Backup database integrity check passed"}
    else:
        return {"status": "invalid", "database": "backup", "message": "Backup database integrity check failed"}