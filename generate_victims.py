import random
from faker import Faker
from wallets import create_wallet
from db import SessionLocal
from models import User

fake = Faker()

CITIES = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", 
          "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]

def generate_victims(count=60):
    db = SessionLocal()
    
    for i in range(1, count+1):
        try:
            wallet = create_wallet()
            victim = User(
                name=fake.name(),
                email=f"victim{i}@demo.com",
                password="victim123",  # Generic password
                city=random.choice(CITIES),
                public_key=wallet["public_key"],
                secret_key=wallet["secret_key"]
            )
            db.add(victim)
            db.commit()
            print(f"✅ Created victim {i}/{count}: {victim.email} in {victim.city}")
        except Exception as e:
            db.rollback()
            print(f"❌ Failed victim {i}: {str(e)}")
    
    db.close()

if __name__ == "__main__":
    print("🚀 Generating 60 dummy victims...")
    generate_victims(60)
    print("🎉 Demo population complete!")