# backend/wallets.py
from stellar_sdk import Keypair
import requests  # 👈 New import
from time import sleep  # 👈 For rate limiting

def create_wallet():
    """Generates AND funds a new wallet automatically"""
    wallet = Keypair.random()
    
    # Step 1: Try Friendbot first (free testnet funding)
    friendbot_url = f"https://friendbot.stellar.org?addr={wallet.public_key}"
    
    try:
        response = requests.get(friendbot_url)
        if response.status_code == 200:
            print(f"✅ Funded wallet via Friendbot: {wallet.public_key}")
        else:
            print(f"⚠️ Friendbot failed. Status: {response.status_code}")
            # Fallback to admin funding if you implement it later
            # fund_from_admin(wallet.public_key)  
    except Exception as e:
        print(f"🚨 Funding error: {str(e)}")
        print(f"👉 MANUAL FUNDING REQUIRED: {friendbot_url}")

    # Rate limiting (Friendbot allows ~5 requests/minute)
    sleep(15)  # 👈 Adjust based on your expected registration rate
    
    return {
        "public_key": wallet.public_key,
        "secret_key": wallet.secret
    }

# Optional admin funding fallback (uncomment when ready)
# def fund_from_admin(target_public_key, amount="10000"):
#     from stellar_sdk import Server, TransactionBuilder, Network, Asset
#     from aid_service import RELIEF_ADMIN_SECRET  # Import your admin keys
#     server = Server("https://horizon-testnet.stellar.org")
#     source = Keypair.from_secret(RELIEF_ADMIN_SECRET)
#     # ... (rest of the funding logic from previous example)

if __name__ == "__main__":
    # Test wallet creation + funding
    wallet = create_wallet()
    print("\n🔑 New Wallet Details:")
    print("Public Key:", wallet["public_key"])
    print("Secret Key:", wallet["secret_key"])
    print(f"Check funding: https://stellar.expert/explorer/testnet/account/{wallet['public_key']}")