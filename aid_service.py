# backend/aid_service.py
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset
from aid_logger import log_aid_transaction  # 🔥 Import logger

server = Server("https://horizon-testnet.stellar.org")
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

RELIEF_ADMIN_SECRET = "SAR3ZSEMATANTB4R2QACD44RRJ7IWZHYQABFCLNMNILM3TUVD3G3GT47"
RELIEF_ADMIN_PUBLIC = "GD5HHKKRQGC3I6J23RH7PD4TAKKHSEYU67YD723DTUWDUPX5TBUWNLTI"

ASSET = Asset.native()  # Using native XLM for now (you can create RELIEF token later if time allows)

def send_aid(destination_wallet, amount="10", disaster_type=None, location=None):
    source = Keypair.from_secret(RELIEF_ADMIN_SECRET)
    source_account = server.load_account(account_id=source.public_key)

    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=network_passphrase,
            base_fee=100
        )
        .append_payment_op(destination=destination_wallet, asset=ASSET, amount=amount)
        .set_timeout(30)
        .build()
    )

    transaction.sign(source)
    response = server.submit_transaction(transaction)
    print(f"✅ Aid sent! Transaction hash: {response['hash']}")

    # 🔥 Log the transaction
    log_aid_transaction(
        wallet=destination_wallet,
        amount=amount,
        disaster=disaster_type if disaster_type else "Unknown",
        location=location if location else "Unknown",
        tx_hash=response["hash"]
    )

    return response
