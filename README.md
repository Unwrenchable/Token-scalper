# Token Scalper Bot 🚀🥷🤖📊

## ☢️ Overseer Bot AI - Vault 77

<div align="center">

![Vault-Tec](https://img.shields.io/badge/VAULT--TEC-77-green?style=for-the-badge)
![Status](https://img.shields.io/badge/STATUS-OPERATIONAL-green?style=for-the-badge)
![Python](https://img.shields.io/badge/PYTHON-3.9%2B-blue?style=for-the-badge)

**A Fallout-themed Twitter bot with cryptocurrency intelligence**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Deployment](#-deployment)

</div>

---

## Ecosystem Overview

**Token-scalper** is the core automated trading and scam-detection engine in a multi-bot ecosystem:

- Scans blockchains for new tokens, scams, and rugpulls.
- Trades and manages positions automatically.
- Reports all findings via webhooks to:
  - The Twitter bot ([overseer-bot-ai](https://github.com/Unwrenchable/overseer-bot-ai)) for public alerts.
  - The dashboard UI ([overseer-bot-ui](https://github.com/Unwrenchable/overseer-bot-ui)) for human monitoring and manual checks.

**This bot does not post to Twitter or provide a web UI. It is designed to run independently and report to other services.**

**Ecosystem Diagram:**
```
+-------------------+      webhook/API      +-------------------+
|   Token-scalper   |  ------------------>  |  overseer-bot-ai  |
| (scans, detects)  |                       | (posts to Twitter)|
+-------------------+                       +-------------------+
         |                                         ^
         | webhook/API                              |
         v                                         |
+-------------------+      fetch/display     +-------------------+
| overseer-bot-ui   |  <------------------  |  overseer-bot-ai  |
| (dashboard)       |                       | (API)             |
+-------------------+                       +-------------------+
```

### Ecosystem Setup

For detailed instructions on setting up the complete ecosystem with all three bots communicating:

📖 **[ECOSYSTEM_SETUP.md](ECOSYSTEM_SETUP.md)** - Complete guide for deploying and wiring all bots together

📖 **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - API endpoints and webhook event schemas

Key features of ecosystem integration:
- **Unified Event Broadcasting**: Automatic alerts to all connected bots
- **Heartbeat Monitoring**: Real-time status tracking across the ecosystem  
- **Webhook Authentication**: Secure API key and shared secret support
- **Standardized Events**: Common schema for all inter-bot communication
- **Health Checks**: Status endpoints for monitoring system health

---

> **🔐 SECURITY NOTICE**: This bot now supports environment variables for storing sensitive data securely. **ALWAYS use `.env` files for private keys and RPC URLs.** Never commit sensitive data to Git!

---

## Ecosystem Overview

**Token-scalper** is the core automated trading and scam-detection engine in a multi-bot ecosystem:

- Scans blockchains for new tokens, scams, and rugpulls.
- Trades and manages positions automatically.
- Reports all findings via webhooks to:
  - The Twitter bot ([overseer-bot-ai](https://github.com/Unwrenchable/overseer-bot-ai)) for public alerts.
  - The dashboard UI ([overseer-bot-ui](https://github.com/Unwrenchable/overseer-bot-ui)) for human monitoring and manual checks.

**This bot does not post to Twitter or provide a web UI. It is designed to run independently and report to other services.**

**Ecosystem Diagram:**
```
+-------------------+      webhook/API      +-------------------+
|   Token-scalper   |  ------------------>  |  overseer-bot-ai  |
| (scans, detects)  |                       | (posts to Twitter)|
+-------------------+                       +-------------------+
         |                                         ^
         | webhook/API                              |
         v                                         |
+-------------------+      fetch/display     +-------------------+
| overseer-bot-ui   |  <------------------  |  overseer-bot-ai  |
| (dashboard)       |                       | (API)             |
+-------------------+                       +-------------------+
```

### Ecosystem Setup

For detailed instructions on setting up the complete ecosystem with all three bots communicating:

📖 **[ECOSYSTEM_SETUP.md](ECOSYSTEM_SETUP.md)** - Complete guide for deploying and wiring all bots together

📖 **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - API endpoints and webhook event schemas

Key features of ecosystem integration:
- **Unified Event Broadcasting**: Automatic alerts to all connected bots
- **Heartbeat Monitoring**: Real-time status tracking across the ecosystem  
- **Webhook Authentication**: Secure API key and shared secret support
- **Standardized Events**: Common schema for all inter-bot communication
- **Health Checks**: Status endpoints for monitoring system health

---

A sophisticated cryptocurrency trading bot that monitors for new token launches, automatically buys promising tokens, and sells them for profit using a responsible selling strategy that prevents price crashes ("killing charts"). Features advanced rug pull protection, moonshot position retention, **multi-wallet/multi-chain support**, **ninja mode for stealth operation**, **🤖 AI-powered token analysis**, **📊 real-time monitoring dashboard**, and **📱 social media integration**.

## Features ✨

- **📊 Real-Time Monitoring Dashboard** (NEW):
  - Web-based interface for live position tracking
  - Analytics visualization (trades, profits, rug pulls avoided)
  - Developer reputation tracking across projects
  - Real-time alerts and notifications
- **👥 Developer Reputation Tracking** (NEW):
  - Track developers across multiple projects
  - Automatic reputation scoring
  - Flag scam developers and rug pulls
  - Persistent developer database
- **📱 Social Media Integration** (NEW):
  - Auto-post alerts to Twitter about suspicious tokens
  - Rug pull warnings to protect community
  - High-potential token notifications
  - Integration with overseer-bot-ai (atomicfizzcaps.xyz)
- **🎯 Token Opportunity Scorer** (NEW):
  - Multi-factor analysis (liquidity, safety, developer, sentiment)
  - "Ape-worthy" token identification
  - Configurable scoring weights
  - Risk vs reward assessment
- **🤖 AI-Powered Token Analysis** (NEW):
  - Advanced risk assessment using AI (OpenAI GPT-4 or Anthropic Claude)
  - Intelligent contract analysis to detect hidden threats
  - Social sentiment analysis for market timing
  - AI-enhanced trading recommendations
  - Detects sophisticated scam patterns that traditional checks miss
- **🔍 Automated Token Discovery**: Continuously scans blockchain for new token launches
- **🛡️ Comprehensive Safety Checks**: 
  - Honeypot detection
  - Liquidity verification
  - Buy/sell tax analysis
  - Contract verification checking
  - Holder count validation
  - **AI risk scoring** (optional)
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

### 7. AI-Powered Token Analysis 🤖

**The cutting-edge feature** - Use AI to analyze tokens before buying:

- **Smart Contract Analysis**: AI examines contract code for hidden threats
- **Risk Scoring**: Intelligent risk assessment (0-100) combining multiple factors
- **Sentiment Analysis**: Evaluates social signals and community strength
- **Pattern Detection**: Identifies sophisticated scam patterns that basic checks miss
- **Trading Recommendations**: AI provides buy/avoid/monitor recommendations with confidence scores

**How AI Analysis Works:**
1. Token is discovered and passes basic safety checks
2. Bot sends token data to AI API (OpenAI GPT-4 or Anthropic Claude)
3. AI analyzes:
   - Contract code patterns and potential vulnerabilities
   - Token economics and distribution
   - Social sentiment indicators
   - Historical patterns of similar tokens
4. AI provides:
   - Risk score (0-100, lower is safer)
   - Sentiment score (0-100, higher is more positive)
   - Specific red flags or positive signals
   - Buy/avoid/monitor recommendation
5. Bot combines AI insights with traditional checks for final decision

**What AI Can Detect:**
- Hidden mint functions that could dilute holders
- Complex rug pull mechanisms
- Suspicious ownership patterns
- Abnormal token distribution
- Social engineering red flags
- Community strength indicators
- Hype vs substance analysis

**AI Safety Integration:**
- If AI risk score > 70: Token is rejected even if traditional checks pass
- If AI recommends "avoid": Trade is skipped
- AI warnings are logged for review
- Works alongside traditional safety checks for defense in depth

**Why This Matters:**
- Traditional checks catch obvious scams
- AI catches sophisticated, hidden threats
- Better protection = more profit, fewer losses
- Learn from AI insights to improve your strategy

This approach:
- ✅ Maximizes your profits by avoiding price crashes
- ✅ Protects you from rug pulls
- ✅ Captures moonshot opportunities
- ✅ Preserves profits in stablecoin
- ✅ Times base currency re-entries for compound gains
- ✅ Detects sophisticated scams before you invest
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

3. **🔐 Configure wallets securely (IMPORTANT for safety):**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values
nano .env  # or use your preferred editor
```

4. Configure bot settings:
```bash
cp config.example.json config.json
# Edit config.json for trading parameters (NOT for sensitive data)
```

## Configuration ⚙️

### 🔐 Security-First Configuration (NEW!)

**IMPORTANT**: For maximum security, store sensitive data in `.env` file, NOT in `config.json`!

### Step 1: Configure Wallets in .env (Secure Method) ⭐ RECOMMENDED

Edit your `.env` file with your actual wallet information:

```bash
# Wallet 1 - Ethereum
WALLET_1_NAME="My Ethereum Wallet"
WALLET_1_RPC_URL="https://mainnet.infura.io/v3/YOUR_ACTUAL_INFURA_KEY"
WALLET_1_CHAIN_ID=1
WALLET_1_PRIVATE_KEY="your_actual_private_key_here"

# Wallet 2 - BSC (Optional)
WALLET_2_NAME="My BSC Wallet"
WALLET_2_RPC_URL="https://bsc-dataseed.binance.org/"
WALLET_2_CHAIN_ID=56
WALLET_2_PRIVATE_KEY="your_actual_private_key_here"

# Add more wallets as needed (WALLET_3_, WALLET_4_, etc.)
```

**Why use .env?**
- ✅ `.env` is in `.gitignore` - won't be committed to Git
- ✅ Separates sensitive data from configuration
- ✅ Industry standard for managing secrets
- ✅ Easy to rotate keys without changing code
- ✅ Can use different `.env` files for different environments

**Security Best Practices:**
- 🔒 **NEVER commit your .env file** to Git
- 🔒 **NEVER share your private keys** with anyone
- 🔒 **Use separate wallets** for bot trading (not your main wallet)
- 🔒 **Keep backups** of your .env file in a secure location
- 🔒 **Rotate keys regularly** if you suspect exposure
- 🔒 **Use hardware wallets** or key management services in production

### Step 2: Configure Trading Parameters in config.json

The `config.json` file should only contain non-sensitive trading parameters:

### Legacy: Multi-Wallet Configuration in config.json (Less Secure)

⚠️ **NOT RECOMMENDED**: If you must use config.json for wallets (legacy mode):

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

### AI Analysis Settings (NEW!) 🤖
```json
"ai_analysis": {
  "enabled": false,                    // Enable AI-powered analysis
  "provider": "openai",                // "openai" or "anthropic"
  "model": "gpt-4",                    // Model to use (gpt-4, gpt-3.5-turbo, claude-3-opus, etc.)
  "api_key": "",                       // API key (better to use .env: AI_API_KEY)
  "max_tokens": 500,                   // Max tokens per AI response
  "temperature": 0.3,                  // AI creativity (0.0-1.0, lower = more consistent)
  "risk_threshold": 70,                // Reject tokens with AI risk score > 70
  "min_sentiment_score": 40            // Minimum sentiment score to consider
}
```

**Setting up AI Analysis:**

1. **Get an API Key**:
   - For OpenAI: Visit https://platform.openai.com/api-keys
   - For Anthropic: Visit https://console.anthropic.com/

2. **Add to .env file** (RECOMMENDED):
   ```bash
   AI_API_KEY="your_api_key_here"
   ```
   Note: Adding an API key to .env does NOT auto-enable AI. You must still set `"enabled": true` in config.json.

3. **Enable in config.json**:
   ```json
   "ai_analysis": {
     "enabled": true,
     "provider": "openai",
     "model": "gpt-4"
   }
   ```

4. **Configure risk thresholds**:
   - `risk_threshold`: Tokens with AI risk score above this are rejected (default: 70)
   - `min_sentiment_score`: Minimum sentiment score to consider buying (default: 40)
   - `temperature`: Controls AI creativity/consistency (0.0 = deterministic, 1.0 = creative, default: 0.3)

**AI Cost Considerations:**
- OpenAI GPT-4: ~$0.03-0.06 per token analysis
- OpenAI GPT-3.5: ~$0.001-0.002 per token analysis (faster, cheaper, less accurate)
- Anthropic Claude: ~$0.01-0.03 per token analysis
- Costs are per token analyzed, so budget accordingly
- AI analysis happens before buying, potentially saving you from bad investments

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

### CLI Commands 💻

The bot includes a CLI interface for various operations:

```bash
# Show help and available commands
python main.py --help

# Run the bot with trading
python main.py run

# Search for airdrop opportunities
python main.py airdrops

# Generate new wallets
python main.py genwallets

# Run as web service with dashboard (for deployment)
python main.py web
```

### Deployment as Web Service 🌐

The bot can run as a web service with a monitoring dashboard, perfect for deployment to platforms like **Render**, **Heroku**, **Railway**, or **DigitalOcean**.

> **📘 For complete deployment instructions including Render Blueprint setup, see [DEPLOYMENT.md](DEPLOYMENT.md)**

**Key Features:**
- Automatically detects deployment environment via `PORT` environment variable
- Uses production-grade **Gunicorn WSGI server** automatically
- Runs monitoring dashboard on configurable port
- Binds to `0.0.0.0` for external access
- Auto-scales workers based on available CPU cores
- Keeps service alive for continuous monitoring

**Automatic Detection:**
When the `PORT` environment variable is set (as is common on deployment platforms), the bot automatically starts in web service mode using Gunicorn:

```bash
# On Render/Heroku, this happens automatically:
PORT=10000 python main.py
# Output: Detected PORT environment variable - running in web service mode
# Output: 🔧 Using Gunicorn production WSGI server
# Dashboard starts on http://0.0.0.0:10000
```

**Production Deployment (Recommended):**
For production environments, use Gunicorn directly with the WSGI entry point:
```bash
# This is the recommended command for Render, Heroku, etc.
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 wsgi:application
```

This command is already configured in:
- `render.yaml` (for Blueprint deployment on Render)
- `Procfile` (for Heroku and other platforms)

See [DEPLOYMENT.md](DEPLOYMENT.md) for platform-specific setup instructions.

**Manual Web Service Mode:**
```bash
# Explicitly run as web service
python main.py web

# With custom config
python main.py --config my-config.json web
```

**Deployment Platforms:**
- **Render.com**: Use Blueprint deployment (see [DEPLOYMENT.md](DEPLOYMENT.md#rendercom))
- **Heroku**: Uses Procfile with Gunicorn
- **Railway**: Compatible with PORT-based services
- **Docker**: Expose port in Dockerfile and docker-compose

> **⚠️ Important:** If deploying to Render, use the Blueprint method or ensure the Dashboard "Start Command" field is empty. See [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting) if you encounter the error: `ImportError: Failed to find application`

**Dashboard Access:**
Once deployed, the dashboard provides:
- Real-time position monitoring
- Wallet balance tracking
- Recent alerts and notifications
- Developer reputation stats
- Performance analytics
- Webhook endpoints for ecosystem integration

**Environment Variables for Deployment:**
```bash
PORT=10000                    # Port for web service (auto-detected)
FLASK_SECRET_KEY=your-secret  # Flask session secret
ECOSYSTEM_API_KEY=your-key    # For webhook authentication
WEB_CONCURRENCY=4            # Number of Gunicorn workers (optional, auto-calculated)
GUNICORN_TIMEOUT=120         # Worker timeout in seconds (default: 120)
USE_GUNICORN=true            # Use Gunicorn server (accepts: true/1/yes or false/0/no)
```

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

- **AI-Powered Risk Assessment**: Advanced threat detection using machine learning (NEW! 🤖)
- **Honeypot Detection**: Verifies tokens can be sold before buying
- **Liquidity Checks**: Ensures sufficient liquidity exists
- **Tax Analysis**: Validates buy/sell taxes are reasonable
- **Contract Verification**: Prefers verified contracts
- **Holder Analysis**: Checks for minimum holder count
- **Stop Loss**: Automatically exits losing positions
- **Position Limits**: Caps maximum investment per token
- **Dev Monitoring**: Tracks developer wallet activity (NEW!)
- **Rug Pull Detection**: Exits before major dumps (NEW!)
- **AI Sentiment Analysis**: Evaluates market sentiment and social signals (NEW! 🤖)

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
- **AI analysis results** (NEW! 🤖)
- **AI risk scores and recommendations** (NEW! 🤖)
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
- **`safety_checker.py`**: Token safety analysis (AI-enhanced)
- **`ai_analyzer.py`**: AI-powered token analysis and risk assessment (NEW! 🤖)
- **`dex_trader.py`**: DEX trading operations
- **`wallet_monitor.py`**: Dev wallet tracking and rug protection (NEW!)
- **`profit_manager.py`**: USDC conversion and base currency timing (NEW!)
- **`config_loader.py`**: Configuration loading with environment variable support
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
- [x] **AI-powered token analysis** 🤖 (COMPLETED!)
- [x] **Web dashboard for monitoring** 📊 (COMPLETED!)
- [x] **Developer reputation tracking** 👥 (COMPLETED!)
- [x] **Social media integration (Twitter)** 📱 (COMPLETED!)
- [x] **Token opportunity scoring** 🎯 (COMPLETED!)
- [ ] Telegram notifications for alerts
- [ ] Discord webhook integration
- [ ] Advanced AI models for price prediction
- [ ] AI-based optimal exit timing
- [ ] Machine learning from historical trades
- [ ] Multi-DEX support
- [ ] Backtesting framework
- [ ] Portfolio management
- [ ] Gas optimization

---

## 📚 Additional Documentation

- **[Monitoring & Analytics Guide](MONITORING_GUIDE.md)** - Complete guide for dashboard, developer tracking, and social media integration
- **[Security Setup Guide](SECURITY_SETUP.md)** - Security best practices and setup instructions

---

**Remember**: This bot's key features are:
1. **Real-time monitoring** - Track everything with live dashboard 📊
2. **Developer tracking** - Identify scam developers before you invest 👥
3. **Social alerts** - Warn community about rug pulls and find gems 📱
4. **AI-powered analysis** - Advanced threat detection and risk assessment 🤖
5. **Responsible selling** - Protects your profits AND the market health
6. **Rug pull protection** - Exits before devs dump on you
7. **Moonshot strategy** - Keeps some tokens for explosive gains
8. **USDC profit management** - Preserves profits and times market re-entries

Trade smart, trade safe! 🎯🛡️🚀💵🤖📊
