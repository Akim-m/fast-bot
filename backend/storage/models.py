from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, DateTime
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)

class Inventory(Base):
    __tablename__ = "inventory"
    item_id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
