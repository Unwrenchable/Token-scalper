# Quick Start Guide - Secure Configuration 🔐

## TL;DR - Get Started in 3 Steps

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env with your wallet info:**
   ```bash
   nano .env  # or use your favorite editor
   ```
   
   Add at minimum:
   ```
   WALLET_1_NAME="My Wallet"
   WALLET_1_RPC_URL="https://mainnet.infura.io/v3/YOUR_KEY"
   WALLET_1_CHAIN_ID=1
   WALLET_1_PRIVATE_KEY="your_actual_private_key"
   ```

3. **Run the bot:**
   ```bash
   python scalper_bot.py
   ```

## Why Use .env Files?

❌ **BAD** - Storing in config.json:
- Can accidentally commit to Git
- Visible in config file
- Hard to rotate keys
- Not standard security practice

✅ **GOOD** - Storing in .env:
- Never committed to Git (in .gitignore)
- Separate from code
- Easy to rotate
- Industry standard
- Can have different .env for dev/prod

## Security Checklist

- [ ] Copied .env.example to .env
- [ ] Added my actual private keys to .env (NOT config.json)
- [ ] Verified .env is in .gitignore
- [ ] Never shared or committed .env file
- [ ] Using separate wallet for bot (not my main wallet)
- [ ] Backed up .env file securely (offline)

## Multiple Wallets Example

```bash
# Ethereum
WALLET_1_NAME="ETH Wallet"
WALLET_1_RPC_URL="https://mainnet.infura.io/v3/YOUR_KEY"
WALLET_1_CHAIN_ID=1
WALLET_1_PRIVATE_KEY="eth_private_key_here"

# Binance Smart Chain
WALLET_2_NAME="BSC Wallet"
WALLET_2_RPC_URL="https://bsc-dataseed.binance.org/"
WALLET_2_CHAIN_ID=56
WALLET_2_PRIVATE_KEY="bsc_private_key_here"

# Polygon
WALLET_3_NAME="Polygon Wallet"
WALLET_3_RPC_URL="https://polygon-rpc.com/"
WALLET_3_CHAIN_ID=137
WALLET_3_PRIVATE_KEY="polygon_private_key_here"
```

## Troubleshooting

**Problem**: Bot says "No wallets configured"
- **Solution**: Make sure your .env file exists and has WALLET_1_* variables

**Problem**: Bot can't connect to RPC
- **Solution**: Check your RPC URL is correct and API key is valid

**Problem**: Transaction fails
- **Solution**: Verify private key is correct and wallet has funds

## Need Help?

See the full README.md for complete documentation.

## 🔒 REMEMBER: NEVER COMMIT YOUR .env FILE!
