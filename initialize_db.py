# backend/initialize_db.py
from db import Base, engine
from models import User  # This import registers the model
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def initialize_database():
    print("♻️ Initializing database...")
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("🗑️ Dropped all tables")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Created all tables")
        
        # Verify
        from sqlalchemy import inspect
        inspector = inspect(engine)
        print("📋 Existing tables:", inspector.get_table_names())
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    initialize_database()