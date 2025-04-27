# backend/aid_logger.py
import json
import os
from datetime import datetime

LOG_FILE = "aid_log.json"

def log_aid_transaction(wallet, amount, disaster, location, tx_hash):
    # Create the log entry
    entry = {
        "wallet": wallet,
        "amount": amount,
        "disaster": disaster,
        "location": location,
        "timestamp": datetime.utcnow().isoformat() + "Z",  # UTC ISO Format
        "transaction_hash": tx_hash
    }
    
    # Read existing logs
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    # Add new entry
    logs.append(entry)

    # Save back to file
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)
