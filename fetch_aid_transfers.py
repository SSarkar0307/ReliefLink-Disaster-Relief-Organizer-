import json
import os

class AidTransferFetcher:
    def __init__(self, file_path="aid_log.json"):
        self.file_path = file_path

    def _load_data(self):
        """Load data from the JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return []

    def get_aid_transfers(self, limit=10):
        """
        Fetch the latest aid transfer entries.
        Args:
            limit (int): Number of latest entries to return (default: 10).
        Returns:
            List of aid transfer entries, sorted by timestamp (newest first).
        """
        # Reload the data from the file each time to ensure freshness
        data = self._load_data()
        
        # Filter entries that have aid transfer data (wallet, amount, transaction_hash)
        aid_transfers = [
            entry for entry in data
            if all(key in entry for key in ["wallet", "amount", "transaction_hash"])
        ]
        # Sort by timestamp (newest first) and limit the number of entries
        aid_transfers = sorted(
            aid_transfers,
            key=lambda x: x.get("timestamp", ""),
            reverse=True
        )[:limit]
        return aid_transfers