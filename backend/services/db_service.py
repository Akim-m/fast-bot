import os
from typing import List, Dict
from sqlalchemy import create_engine, Table, MetaData, select, inspect
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException

DB_FILE = "storage/app.db"
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_FILE}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

metadata = MetaData()

def get_db():
    """Database session generator for dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_table_data(table_name: str) -> List[Dict]:
    """Retrieve all rows from a specified table"""
    try:
        table = Table(table_name, metadata, autoload_with=engine)
    except Exception as e:
        raise HTTPException(
            status_code=404, 
            detail=f"Table '{table_name}' not found: {str(e)}"
        )

    db = SessionLocal()
    try:
        result = db.execute(select(table))
        return [dict(row._mapping) for row in result.fetchall()]
    finally:
        db.close()

def list_tables() -> List[str]:
    """List all tables in the database"""
    inspector = inspect(engine)
    return inspector.get_table_names()

def check_database_health() -> bool:
    """Check if database is accessible and responsive"""
    try:
        db = SessionLocal()
        db.execute(select(1))
        db.close()
        return True
    except Exception:
        return False