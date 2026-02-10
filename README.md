# Token Scalper Bot 🚀🥷

A sophisticated cryptocurrency trading bot that monitors for new token launches, automatically buys promising tokens, and sells them for profit using a responsible selling strategy that prevents price crashes ("killing charts"). Features advanced rug pull protection, moonshot position retention, **multi-wallet/multi-chain support**, and **ninja mode for stealth operation**.

## Features ✨

- **🔍 Automated Token Discovery**: Continuously scans blockchain for new token launches
- **🛡️ Comprehensive Safety Checks**: 
  - Honeypot detection
  - Liquidity verification
  - Buy/sell tax analysis
  - Contract verification checking
  - Holder count validation
- **💰 Smart Buy Logic**: Automatically purchases tokens that meet safety criteria
- **📈 Profit Monitoring**: Real-time tracking of profit/loss for all positions
- **🎯 Intelligent Selling**: 
  - Profit target and stop-loss mechanisms
  - **Responsible selling in chunks** to minimize market impact
  - Configurable delays between sells to prevent chart crashes
  - Price impact calculation and optimization
- **🚨 Rug Pull Protection**:
  - Monitors developer wallet activity
  - Detects dev selling in real-time
  - Auto-exits before major dumps
  - Tracks large holder movements
- **🌙 Moonshot Strategy**:
  - Keeps percentage of tokens for potential 10x+ gains
  - Automatically sells moonshot reserve when target reached
  - Maximizes profits on explosive moves
- **💵 USDC Profit Management**:
  - Auto-converts profits to USDC stablecoin
  - Monitors base currency (ETH/SOL/BNB/etc) for buying opportunities
  - Re-enters base currency during dips
  - Preserves profits and times market entries
- **🌐 Multi-Wallet Multi-Chain Support** (NEW):
  - Support for multiple wallets across different chains
  - Auto-selects wallet with funds
  - Works with ETH, BNB, MATIC, AVAX, FTM, Arbitrum, Optimism
  - Chain-specific DEX routers and stablecoins
- **🥷 Ninja Mode - Concurrent Operation** (NEW):
  - Runs multiple wallets simultaneously in parallel
  - Distributes trades across wallets to avoid detection
  - Randomized delays and trade amounts for stealth
  - Coordinated operation to prevent self-competition
  - Makes bot undetectable to shady developers
- **📊 Detailed Logging**: Complete transaction and profit/loss tracking

## Key Features Explained 🌟

### 1. Responsible Selling 

The bot's signature feature is its **responsible selling mechanism**. Unlike bots that dump entire positions at once (which crashes the price and "kills the chart"), this bot:

1. **Splits sales into multiple chunks** (default: 5 chunks)
2. **Waits between each chunk** (default: 30 seconds) 
3. **Monitors price impact** to ensure each sell doesn't exceed maximum impact percentage
4. **Dynamically adjusts chunk sizes** based on liquidity
5. **Preserves chart health** for other traders

### 2. Rug Pull Protection 🛡️

The bot actively protects you from rug pulls:

- **Dev Wallet Identification**: Automatically identifies developer/team wallets
- **Real-time Monitoring**: Continuously tracks dev wallet balances
- **Sell Detection**: Alerts when devs start dumping tokens
- **Emergency Exit**: Automatically exits position before major rug pulls
- **Multi-level Urgency**: Categorizes threats (low/medium/high/critical)

When dev selling is detected:
- **10%+ sold** → Monitor closely
- **15%+ sold** → Reduce position
- **30%+ sold** → Exit soon (high urgency)
- **50%+ sold** → EXIT IMMEDIATELY (critical)

### 3. Moonshot Strategy 🌙

Don't miss out on massive gains:

- **Keeps 20% of tokens** (configurable) after taking profits
- **Monitors for 10x+ price movement** (configurable multiplier)
- **Automatic moonshot sale** when target reached
- **No moonshot reserve on rug pulls** - sells everything for safety

### 4. USDC Profit Management 💵

Preserve and grow your profits intelligently:

- **Auto-converts to USDC**: Automatically converts 80% of profits to USDC stablecoin (keeps 20% in base currency)
- **Market Timing**: Monitors base currency (ETH, SOL, BNB, etc.) price movements
- **Smart Re-entry**: Automatically buys back base currency during dips
- **Profit Protection**: Locks in gains in stablecoin while waiting for optimal re-entry

**How it works:**
1. You sell tokens for 1 ETH profit
2. Bot converts 0.8 ETH → USDC (keeps 0.2 ETH)
3. Bot monitors ETH price ($3000 → $2700)
4. ETH dips 10% - bot detects opportunity
5. Bot converts USDC back to ETH at lower price
6. You now have more ETH than you started with!

### 5. Multi-Wallet Multi-Chain Support 🌐

Operate across multiple wallets and blockchains:

- **Multiple Wallets**: Configure as many wallets as you want
- **Multi-Chain**: Supports Ethereum, BSC, Polygon, Avalanche, Fantom, Arbitrum, Optimism
- **Auto-Selection**: Automatically selects wallet with funds
- **Chain-Specific**: Uses correct DEX routers and stablecoins for each chain
- **Flexible Funding**: Works with base currency (ETH/BNB/etc) or stablecoin (USDC) funding

**Supported Chains:**
- Ethereum (ETH) - Uniswap V2
- Binance Smart Chain (BNB) - PancakeSwap
- Polygon (MATIC) - QuickSwap
- Avalanche (AVAX) - TraderJoe
- Fantom (FTM) - SpookySwap
- Arbitrum (ETH) - SushiSwap
- Optimism (ETH) - Velodrome

### 6. Ninja Mode - Stealth Operation 🥷

**The ultimate anti-detection feature** - Operate multiple wallets simultaneously:

- **Concurrent Operation**: Runs multiple wallet instances in parallel threads
- **Stealth Distribution**: Distributes trades across wallets to avoid patterns
- **Randomization**: Randomizes delays (1-5s) and trade amounts (±10%)
- **Smart Coordination**: Prevents wallets from competing with each other
- **Load Balancing**: Distributes positions across wallets (max 5 per wallet)
- **Time-Based Logic**: Avoids rapid-fire trades from same wallet
- **Undetectable**: Makes it nearly impossible for shady devs to identify bot activity

**How Ninja Mode Works:**
1. Bot creates separate instance for each wallet
2. Each instance runs independently in its own thread
3. Orchestrator coordinates token discovery (no duplicate scanning)
4. When new token found, selects best wallet for trade
5. Selection uses weighted randomization based on:
   - Current position count (prefer less loaded wallets)
   - Time since last trade (avoid rapid trades from same wallet)
   - Random factor (unpredictable behavior)
6. Applies stealth delay (1-5s random)
7. Randomizes trade amount (±10% variation)
8. Each wallet monitors its own positions independently

**Why This Matters:**
- **Single wallet pattern**: Dev can see repeated buys from same address → DETECTED
- **Ninja mode**: Buys come from different addresses at random intervals → INVISIBLE
- **Result**: You can trade while shady devs can't identify or block you

This approach:
- ✅ Maximizes your profits by avoiding price crashes
- ✅ Protects you from rug pulls
- ✅ Captures moonshot opportunities
- ✅ Preserves profits in stablecoin
- ✅ Times base currency re-entries for compound gains
- ✅ Allows other traders to exit safely
- ✅ Maintains healthy price action
- ✅ Builds sustainable trading reputation

## Installation 📦

1. Clone the repository:
```bash
git clone https://github.com/Unwrenchable/Token-scalper.git
cd Token-scalper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the bot:
```bash
cp config.example.json config.json
```

4. Edit `config.json` with your settings (see Configuration section below)

## Configuration ⚙️

Edit `config.json` with your specific settings:

### Multi-Wallet Configuration (NEW!)
```json
"wallets": [
  {
    "name": "Ethereum Wallet",
    "rpc_url": "https://mainnet.infura.io/v3/YOUR_KEY",
    "chain_id": 1,
    "private_key": "YOUR_PRIVATE_KEY_HERE"
  },
  {
    "name": "BSC Wallet",
    "rpc_url": "https://bsc-dataseed.binance.org/",
    "chain_id": 56,
    "private_key": "YOUR_PRIVATE_KEY_HERE"
  },
  {
    "name": "Polygon Wallet",
    "rpc_url": "https://polygon-rpc.com/",
    "chain_id": 137,
    "private_key": "YOUR_PRIVATE_KEY_HERE"
  }
]
```

**Important Notes:**
- You can add as many wallets as you want
- Each wallet can be on a different chain
- You can use the SAME private key for all chains (one wallet, multiple chains)
- Or use DIFFERENT private keys for different chains (multiple wallets)
- Bot auto-selects wallet with funds
- Works with base currency (ETH/BNB) OR stablecoin (USDC) funding

### Wallet Selection Settings
```json
"wallet_selection": {
  "auto_select_funded": true,        // Auto-select wallet with funds
  "min_balance_usd": 10,             // Minimum $10 to be considered funded
  "prefer_chain_id": null            // Prefer specific chain (null = any)
}
```

### Ninja Mode Settings (NEW!)
```json
"ninja_mode": {
  "enabled": true,                   // Enable concurrent multi-wallet operation
  "max_positions_per_wallet": 5,     // Max positions per wallet
  "stealth_delay_min_seconds": 1,    // Min delay before trade
  "stealth_delay_max_seconds": 5,    // Max delay before trade
  "randomize_amounts": true,         // Randomize trade amounts
  "amount_variation_percent": 10,    // ±10% amount variation
  "coordinate_wallets": true         // Coordinate between wallets
}
```

### Trading Parameters
```json
"trading": {
  "buy_amount_eth": 0.1,               // Amount to invest per token
  "min_liquidity_eth": 5,              // Minimum liquidity required
  "max_buy_tax": 10,                   // Maximum acceptable buy tax %
  "max_sell_tax": 10,                  // Maximum acceptable sell tax %
  "profit_target_percent": 50,         // Take profit at this % gain
  "stop_loss_percent": 30,             // Exit at this % loss
  "max_slippage_percent": 15           // Maximum slippage tolerance
}
```

### Responsible Selling Settings
```json
"selling": {
  "sell_chunks": 5,                    // Number of chunks to split sales
  "chunk_delay_seconds": 30,           // Wait time between chunks
  "max_sell_impact_percent": 5,        // Maximum price impact per chunk
  "keep_percentage_for_moonshot": 20,  // % to keep for moonshot (NEW!)
  "moonshot_multiplier": 10            // Sell when price is 10x entry (NEW!)
}
```

### Rug Pull Protection Settings (NEW!)
```json
"rug_protection": {
  "enable_dev_monitoring": true,       // Enable dev wallet monitoring
  "dev_sell_threshold_percent": 10,    // Alert if dev sells >10%
  "large_sell_threshold_percent": 5,   // Track sells >5% of liquidity
  "max_large_sells_before_exit": 3,    // Exit after 3 large sells
  "monitor_interval_seconds": 10       // How often to check wallets
}
```

### USDC Profit Management Settings (NEW!)
```json
"profit_management": {
  "auto_convert_to_usdc": true,           // Auto-convert profits to USDC
  "keep_base_currency_percent": 20,       // Keep 20% in base currency
  "buy_base_dip_threshold_percent": 10,   // Buy when dipped >10%
  "buy_base_below_avg_percent": 5,        // Buy when 5% below avg
  "base_buyback_percent": 30,             // Convert 30% of USDC per buy
  "min_usdc_for_conversion": 100,         // Min $100 USDC to convert
  "max_usdc_per_conversion": 1000         // Max $1000 per conversion
}
```

### Monitoring Settings
```json
"monitoring": {
  "scan_interval_seconds": 2,          // How often to scan for new tokens
  "min_holder_count": 10,              // Minimum holders required
  "blacklisted_tokens": []             // Tokens to ignore
}
```

### Safety Settings
```json
"safety": {
  "enable_honeypot_check": true,       // Enable honeypot detection
  "min_contract_age_seconds": 0,       // Minimum contract age
  "max_position_size_eth": 1.0         // Maximum investment per token
}
```

## Usage 🚀

### Standard Mode (Single Wallet Selected)
Run the bot with automatic wallet selection:
```bash
python scalper_bot.py
```

The bot will:
1. Connect to all configured wallets
2. Check balances on all chains
3. Auto-select the wallet with most funds
4. Start trading on that chain

### Ninja Mode (Multi-Wallet Concurrent) 🥷
Run the orchestrator for stealth operation:
```bash
python ninja_bot_orchestrator.py
```

The ninja bot will:
1. Create separate bot instance for each wallet
2. Run all instances concurrently in parallel threads
3. Coordinate token discovery across instances
4. Distribute trades across wallets using stealth logic
5. Randomize delays and amounts to avoid detection
6. Monitor all positions across all wallets

**Ninja Mode Output:**
```
🥷 Ninja Bot Orchestrator initialized
Creating 3 bot instances...
✅ Connected to Ethereum wallet: 0x1234...
   Balance: 1.5000 ETH, $500.00 USDC
✅ Connected to BSC wallet: 0x5678...
   Balance: 5.2000 BNB, $200.00 USDC
✅ Connected to Polygon wallet: 0x9abc...
   Balance: 1000.0000 MATIC, $100.00 USDC

🚀 Starting all bot instances...
✅ Started 3 bot instances

🎯 Selected wallet Ethereum:0x1234... for trade
🕐 Stealth delay: 3.47s
📍 New token discovered: 0xToken...
✅ Successfully bought 1000.52 tokens at 0.00001 ETH

================================================================================
🥷 NINJA BOT STATUS
Total Instances: 3
Running: 3
Total Positions: 5
--------------------------------------------------------------------------------
📍 Ethereum:0x1234...
   Chain: Ethereum | Status: running
   Positions: 2 | Balance: 1.4500 ETH
📍 BSC:0x5678...
   Chain: Binance Smart Chain | Status: running
   Positions: 2 | Balance: 5.1000 BNB
📍 Polygon:0x9abc...
   Chain: Polygon | Status: running
   Positions: 1 | Balance: 995.0000 MATIC
================================================================================
```

### Which Mode to Use?

**Use Standard Mode if:**
- You have one wallet or want to trade on one chain
- You're just getting started
- You want simpler operation

**Use Ninja Mode if:**
- You have multiple wallets funded
- You want to avoid detection by shady devs
- You want maximum stealth and distribution
- You can handle more complexity

The bot will:
1. Connect to the blockchain
2. Start scanning for new token launches
3. Analyze tokens for safety
4. Automatically buy tokens that pass checks
5. **Start monitoring dev wallets** for rug pull signals
6. Monitor positions for profit opportunities
7. Sell responsibly when profit targets are hit
8. **Auto-convert profits to USDC** (keeps 20% in base currency)
9. **Keep a portion for moonshots** (unless rug pull detected)
10. **Auto-exit if dev dumping detected**
11. **Monitor base currency for good re-entry points**
12. **Buy back base currency during dips**

## How It Protects You 🛡️

### Normal Profit Taking (No Rug Pull)
1. Token reaches 50% profit target
2. Bot sells 80% in 5 chunks over 2.5 minutes
3. Keeps 20% for potential moonshot
4. Monitors kept tokens for 10x price movement
5. Sells moonshot reserve when 10x reached

### Rug Pull Detected
1. Bot detects dev selling 30%+ of holdings
2. Immediately triggers emergency exit
3. Sells **ALL tokens** including moonshot reserve
4. Uses only 3 chunks with 5-second delays
5. Exits as fast as possible while minimizing slippage

### Moonshot Scenario
1. You took 50% profit and kept 20% of tokens
2. Token price increases 10x from entry
3. Bot automatically sells moonshot reserve
4. You capture massive additional gains

### USDC Profit Management Scenario
1. Bot sells tokens for 2 ETH profit at $3000/ETH = $6000
2. Auto-converts 1.6 ETH to $4800 USDC (keeps 0.4 ETH)
3. ETH price drops to $2700 (10% dip detected)
4. Bot converts $1440 USDC → 0.533 ETH at lower price
5. You now have 0.933 ETH (vs 0.4 ETH if you just held)

## Safety Features 🛡️

The bot includes multiple safety mechanisms:

- **Honeypot Detection**: Verifies tokens can be sold before buying
- **Liquidity Checks**: Ensures sufficient liquidity exists
- **Tax Analysis**: Validates buy/sell taxes are reasonable
- **Contract Verification**: Prefers verified contracts
- **Holder Analysis**: Checks for minimum holder count
- **Stop Loss**: Automatically exits losing positions
- **Position Limits**: Caps maximum investment per token
- **Dev Monitoring**: Tracks developer wallet activity (NEW!)
- **Rug Pull Detection**: Exits before major dumps (NEW!)

## Responsible Trading Philosophy 🌱

This bot is designed for **sustainable and safe trading**:

1. **Don't Kill Charts**: Gradual selling preserves price action
2. **Protect Against Rugs**: Exit before devs dump on you
3. **Capture Moonshots**: Keep some tokens for explosive gains
4. **Consider Other Traders**: Allows community to exit safely
5. **Long-term Thinking**: Healthy charts = better reputation
6. **Calculated Exits**: Price impact optimization
7. **Market Health**: Contributes to overall market stability

## Logging 📝

All activity is logged to:
- `scalper_bot.log` - Detailed file logging
- Console output - Real-time monitoring

Log entries include:
- Token discoveries
- Safety check results
- Buy/sell transactions
- **Dev wallet monitoring** (NEW!)
- **Rug pull alerts** (NEW!)
- **Moonshot tracking** (NEW!)
- **USDC conversions** (NEW!)
- **Base currency buy signals** (NEW!)
- Profit/loss tracking
- Error messages

## Architecture 🏗️

The bot consists of several modules:

- **`scalper_bot.py`**: Main bot logic and orchestration
- **`safety_checker.py`**: Token safety analysis
- **`dex_trader.py`**: DEX trading operations
- **`wallet_monitor.py`**: Dev wallet tracking and rug protection (NEW!)
- **`profit_manager.py`**: USDC conversion and base currency timing (NEW!)
- **`config.json`**: Configuration settings

## Example Scenarios 📖

### Scenario 1: Normal Profitable Trade
```
1. Bot buys token at $0.00001
2. Price increases to $0.000015 (50% profit)
3. Bot sells 80% in chunks over 2.5 minutes
4. Keeps 20% for potential moonshot
5. Price later hits $0.0001 (10x from entry)
6. Bot sells moonshot reserve
7. Final profit: 50% on 80% + 900% on 20% = huge gains!
```

### Scenario 2: Rug Pull Protection
```
1. Bot buys token at $0.00001
2. Bot monitors dev wallet (has 1M tokens)
3. Dev sells 300K tokens (30% of holdings) 
4. Bot detects high urgency rug pull risk
5. Bot immediately exits ALL tokens (no moonshot reserve)
6. Exits at $0.000009 with only -10% loss
7. Token later crashes to $0.000001 (would have been -90% loss)
```

### Scenario 3: Stop Loss
```
1. Bot buys token at $0.00001
2. Price drops to $0.000007 (30% loss)
3. Stop loss triggers
4. Bot sells all tokens in chunks
5. Limits loss to -30% instead of bigger potential loss
```

## Disclaimer ⚠️

**USE AT YOUR OWN RISK**

- Cryptocurrency trading involves significant risk
- This bot is for educational purposes
- Test thoroughly on testnet before using real funds
- Never invest more than you can afford to lose
- Past performance doesn't guarantee future results
- Rug pull protection is not foolproof
- The developers assume no liability for losses

## Security Best Practices 🔒

1. **Never share your private key**
2. **Use a dedicated wallet for bot trading**
3. **Start with small amounts for testing**
4. **Keep your RPC endpoint secure**
5. **Review all configuration before running**
6. **Monitor bot activity regularly**
7. **Keep dependencies updated**
8. **Test rug pull detection on testnet**

## Contributing 🤝

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License 📄

See LICENSE file for details.

## Support 💬

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review logs for error details

## Roadmap 🗺️

Future enhancements:
- [ ] Web dashboard for monitoring
- [ ] Telegram notifications for rug pull alerts
- [ ] Multi-DEX support
- [ ] Advanced ML-based token analysis
- [ ] Backtesting framework
- [ ] Portfolio management
- [ ] Gas optimization
- [ ] Multi-chain support

---

**Remember**: This bot's key features are:
1. **Responsible selling** - Protects your profits AND the market health
2. **Rug pull protection** - Exits before devs dump on you
3. **Moonshot strategy** - Keeps some tokens for explosive gains
4. **USDC profit management** - Preserves profits and times market re-entries

Trade smart, trade safe! 🎯🛡️🚀💵
