# backend/check.py
from db import SessionLocal
from models import User

def check_users():
    db = SessionLocal()
    try:
        users = db.query(User).order_by(User.id).all()
        
        if not users:
            print("⚠️ No users found in database")
            return
            
        print(f"📊 Found {len(users)} users:")
        for i, user in enumerate(users, 1):
            if user:  # Check for None values
                print(f"\nID: {user.id}, Name: {user.name}")
                print(f"Email: {user.email}, City: {user.city}")
                print(f"Public Key: {user.public_key}")
            else:
                print(f"⚠️ Empty record at position {i}")
                
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users()