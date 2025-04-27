# backend/reset_db.py
import os
from db import Base, engine

def reset_database():
    try:
        # Delete database file if exists
        db_file = "relieflink.db"
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"🗑️ Deleted existing database file: {db_file}")
        
        # Create fresh tables
        Base.metadata.create_all(bind=engine)
        print("✅ Created fresh database with all tables")
        
        # Verify
        from sqlalchemy import inspect
        inspector = inspect(engine)
        print("📋 Tables created:", inspector.get_table_names())
        
    except Exception as e:
        print(f"❌ Error resetting database: {str(e)}")
        raise

if __name__ == "__main__":
    reset_database()