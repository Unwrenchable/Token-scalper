"""
Wallet Generator Script
Generates wallets and exports them to .env format for use in the bot.
"""

import os
from eth_account import Account
from dotenv import set_key

NUM_WALLETS = int(os.getenv('NUM_WALLETS', 3))
ENV_PATH = os.getenv('ENV_PATH', '.env')

Account.enable_unaudited_hdwallet_features()

wallets = []
for i in range(1, NUM_WALLETS + 1):
    acct = Account.create()
    wallets.append({
        'name': f'WALLET_{i}',
        'private_key': acct.key.hex(),
        'address': acct.address
    })
    set_key(ENV_PATH, f'WALLET_{i}_PRIVATE_KEY', acct.key.hex())
    set_key(ENV_PATH, f'WALLET_{i}_ADDRESS', acct.address)

print(f"Generated {NUM_WALLETS} wallets and exported to {ENV_PATH}")
