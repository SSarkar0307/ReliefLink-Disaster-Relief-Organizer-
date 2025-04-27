# backend/models.py
from sqlalchemy import Column, Integer, String
from db import Base  # Must import Base from your db.py

class User(Base):
    __tablename__ = "users"  # Must match exactly
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    public_key = Column(String(56), unique=True, nullable=False)
    secret_key = Column(String(56), nullable=False)