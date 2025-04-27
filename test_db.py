# backend/test_db.py
from sqlalchemy import text  # 👈 Add this import
from db import SessionLocal, engine
from models import User

def test_connection():
    db = SessionLocal()
    try:
        # Test connection with proper text() wrapper
        db.execute(text("SELECT 1"))  # 👈 Corrected line
        print("✅ Database connection successful")
        
        # Check if users table exists
        users_count = db.query(User).count()
        print(f"📊 Found {users_count} users in database")
        
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        print("Full error details:")
        import traceback
        traceback.print_exc()  # 👈 This will show the complete error stack
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()