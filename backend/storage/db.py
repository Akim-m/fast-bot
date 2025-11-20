import sqlite3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.storage.models import Base

DB_FILE = "storage/app.db"
SQL_FOLDER = "storage/models"

os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

def get_sqlite_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    sql_files = ["table.sql", "inventory_table.sql"]

    conn = get_sqlite_connection()
    cursor = conn.cursor()

    for file_name in sql_files:
        sql_path = os.path.join(SQL_FOLDER, file_name)
        if os.path.exists(sql_path):
            with open(sql_path, "r") as f:
                cursor.executescript(f.read())

    conn.commit()
    conn.close()

DATABASE_URL = f"sqlite:///{DB_FILE}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
