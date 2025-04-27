from stellar_sdk import Server

server = Server("https://horizon-testnet.stellar.org")

def get_balance(public_key):
    try:
        print(f"🔍 Checking balance for: {public_key}")
        account = server.accounts().account_id(public_key).call()
        balances = account['balances']
        
        print(f"✅ Account exists! Balances:")
        for balance in balances:
            print(f"  - Asset: {balance['asset_type']}, Balance: {balance['balance']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("ℹ️ Possible solutions:")
        print("1. Fund the wallet first: https://friendbot.stellar.org/?addr=YOUR_PUBLIC_KEY")
        print("2. Verify the public key is correct")

if __name__ == "__main__":
    public_key = "GARD5LRM5TLLZVOPWRKOOBXK3VIES6P2WIO4PI5ZCWSHTHLOY23ZNWII"  # Replace with your key
    get_balance(public_key)