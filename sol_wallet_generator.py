"""
Solana Wallet Generator Script
Generates Solana wallets and exports them to .env format for use in the bot.
"""

import os
from solders.keypair import Keypair
import solders.pubkey
from dotenv import set_key
import base58

NUM_WALLETS = int(os.getenv('NUM_SOL_WALLETS', 3))
ENV_PATH = os.getenv('ENV_PATH', '.env')


for i in range(1, NUM_WALLETS + 1):
    kp = Keypair()
    privkey_bytes = kp.to_bytes()
    privkey_b58 = base58.b58encode(privkey_bytes).decode()
    pubkey = str(kp.pubkey())
    set_key(ENV_PATH, f'SOL_WALLET_{i}_PRIVATE_KEY', privkey_b58)
    set_key(ENV_PATH, f'SOL_WALLET_{i}_ADDRESS', pubkey)
    print(f"SOL_WALLET_{i}_ADDRESS={pubkey}")
    print(f"SOL_WALLET_{i}_PRIVATE_KEY={privkey_b58}")

print(f"Generated {NUM_WALLETS} Solana wallets and exported to {ENV_PATH}")
