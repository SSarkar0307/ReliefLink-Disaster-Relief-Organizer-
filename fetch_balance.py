from stellar_sdk import Server
from stellar_sdk.exceptions import NotFoundError, ConnectionError

server = Server("https://horizon-testnet.stellar.org")

def get_balance(public_key):
    try:
        # Validate public key format
        if not public_key.startswith('G') or len(public_key) != 56:
            raise ValueError("Invalid public key format")

        account = server.accounts().account_id(public_key).call()
        balances = account['balances']
        
        # Sum all native (XLM) balances
        total = sum(
            float(b['balance']) for b in balances if b['asset_type'] == 'native'
        )
        return round(total, 2)

    except ValueError as e:
        print(f"Key error: {e}")
        return 0
    except NotFoundError:
        print("Account not found on Stellar network")
        return 0
    except ConnectionError:
        print("Failed to connect to Stellar Horizon")
        return 0
    except Exception as e:
        print(f"Stellar error: {e}")
        return 0