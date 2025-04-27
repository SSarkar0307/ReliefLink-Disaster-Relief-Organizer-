# routes/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from db import SessionLocal, engine
from models import User
from wallets import create_wallet
import logging
import traceback

router = APIRouter()
logger = logging.getLogger(__name__)

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    city: str

    @field_validator('email')
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower().strip()

@router.post("/register")
async def register_user(user: RegisterRequest):
    """Register a new user with blockchain wallet"""
    db: Session = SessionLocal()
    try:
        # Verify database connection
        db.execute("SELECT 1")
        
        # Validate input
        if not all([user.name.strip(), user.email, user.city.strip()]):
            raise HTTPException(422, "All fields are required")

        # Check for existing user
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(409, "Email already registered")

        # Create wallet
        wallet = create_wallet()
        if not wallet:
            raise HTTPException(500, "Wallet creation failed")

        # Create user object
        user_obj = User(
            name=user.name.strip(),
            email=user.email,
            password=user.password,
            city=user.city.strip().title(),
            public_key=wallet["public_key"],
            secret_key=wallet["secret_key"]
        )

        # Database operations with explicit transaction
        db.begin()
        try:
            db.add(user_obj)
            db.commit()
            db.refresh(user_obj)
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity Error: {str(e)}\n{traceback.format_exc()}")
            raise HTTPException(400, "Database integrity error (possible duplicate)")
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"SQLAlchemy Error: {str(e)}\n{traceback.format_exc()}")
            raise HTTPException(500, "Database operation failed")

        return {
            "status": "success",
            "user_id": user_obj.id,
            "wallet_address": user_obj.public_key
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}\n{traceback.format_exc()}")
        if db.in_transaction():
            db.rollback()
        raise HTTPException(500, "Internal server error")
    finally:
        db.close()