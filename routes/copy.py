from fastapi import APIRouter, HTTPException
from db import SessionLocal
from models import User
from sqlalchemy.orm import Session
from wallets import create_wallet
from pydantic import BaseModel

router = APIRouter()

# Pydantic model for JSON body
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    city: str

@router.post("/register")
async def register_user(user: RegisterRequest):  # 👈 Accepts JSON via Pydantic model
    db = SessionLocal()
    wallet = create_wallet()

    user_obj = User(
        name=user.name,
        email=user.email,
        password=user.password,  # Note: Hash this later!
        city=user.city,
        public_key=wallet["public_key"],
        secret_key=wallet["secret_key"]
    )

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return {"msg": "User registered successfully", "wallet_public_key": user_obj.public_key}