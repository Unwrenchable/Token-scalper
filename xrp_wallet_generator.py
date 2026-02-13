"""
Ripple (XRP) Wallet Generator Script
Generates Ripple wallets and exports them to .env format for use in the bot.
"""

import os
from dotenv import set_key
import secrets
import xrpl.wallet

NUM_WALLETS = int(os.getenv('NUM_XRP_WALLETS', 3))
ENV_PATH = os.getenv('ENV_PATH', '.env')

for i in range(1, NUM_WALLETS + 1):
    wallet = xrpl.wallet.Wallet.create()
    set_key(ENV_PATH, f'XRP_WALLET_{i}_SEED', wallet.seed)
    set_key(ENV_PATH, f'XRP_WALLET_{i}_ADDRESS', wallet.classic_address)
    print(f"XRP_WALLET_{i}_ADDRESS={wallet.classic_address}")
    print(f"XRP_WALLET_{i}_SEED={wallet.seed}")

print(f"Generated {NUM_WALLETS} Ripple wallets and exported to {ENV_PATH}")
