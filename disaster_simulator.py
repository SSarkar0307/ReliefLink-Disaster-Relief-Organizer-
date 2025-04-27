import random
import time
import threading
from fastapi import APIRouter
from aid_service import send_aid
from db import SessionLocal  # Import database session
from models import User  # Import User model

router = APIRouter()
alerts = []  # Local list to store disaster events

def generate_disasters():
    disaster_types = ["flood", "earthquake", "fire", "cyclone"]
    locations = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore",
                "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]

    while True:
        alert = {
            "location": random.choice(locations),
            "disaster": random.choice(disaster_types),
            "level": round(random.uniform(1.0, 10.0), 1),
            "timestamp": time.time()
        }
        print(f"Generated alert: {alert}")
        alerts.append(alert)

        # 🔥 Updated Aid Trigger Logic (Database Query)
        if alert["level"] >= 7:
            db = SessionLocal()
            try:
                # Query victims in affected city
                victims = db.query(User).filter(User.city == alert["location"]).all()
                
                print(f"🚨 Found {len(victims)} victims in {alert['location']}")
                
                for victim in victims:
                    try:
                        print(f"🚑 Sending aid to {victim.name} ({victim.public_key})")
                        send_aid(
                            destination_wallet=victim.public_key,
                            disaster_type=alert["disaster"],
                            location=alert["location"]
                        )
                    except Exception as e:
                        print(f"⚠️ Failed to aid {victim.name}: {str(e)}")
                        
            except Exception as e:
                print(f"❌ Database error: {str(e)}")
            finally:
                db.close()  # Always close the session

        time.sleep(15)

@router.get("/alerts")
async def get_alerts():
    return alerts