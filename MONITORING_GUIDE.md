# Monitoring, Analytics & Social Media Integration

## Overview

The Token Scalper Bot now includes comprehensive monitoring, analytics, and social media integration capabilities. These features provide real-time visibility into bot operations, track developer reputations across projects, alert the community about suspicious tokens, and identify high-potential opportunities.

## New Features

### 1. 📊 Web-Based Monitoring Dashboard

A real-time web dashboard for monitoring bot activity and analytics.

**Features:**
- Live position tracking
- Real-time alerts and notifications
- Analytics visualization (trades, profits, rug pulls avoided)
- Developer tracking statistics
- Clean, modern UI with auto-refresh

**Setup:**
```json
"dashboard": {
  "enabled": true,
  "host": "127.0.0.1",  // Use "0.0.0.0" for external access
  "port": 5000
}
```

**Access:**
- Start bot and dashboard will be available at `http://127.0.0.1:5000`
- Dashboard runs in a separate thread, doesn't interfere with trading

**Dashboard Sections:**
1. **Analytics** - Total trades, success rate, rug pulls avoided, total profit
2. **Developer Tracking** - Tracked/flagged developers, tracked/rugged projects
3. **Active Positions** - Real-time position monitoring with P/L
4. **Recent Alerts** - Latest notifications (rug pulls, suspicious tokens, opportunities)

### 2. 👥 Developer Reputation Tracker

Tracks developer wallets across multiple projects and builds reputation scores.

**Features:**
- Persistent developer database (JSON storage)
- Multi-project developer linking
- Reputation scoring (0-100)
- Automatic flagging of scam developers
- Project-to-developer mapping
- Rug pull and scam counting

**How It Works:**
```python
from dev_reputation_tracker import DevReputationTracker

tracker = DevReputationTracker()

# Register a new project
tracker.register_project(
    token_address="0x123...",
    token_name="MyToken",
    dev_addresses=["0xdev1...", "0xdev2..."]
)

# Flag a rug pull
tracker.flag_project("0x123...", "rug_pull", "Dev sold 50% of holdings")

# Check if developer is suspicious
is_suspicious = tracker.is_developer_suspicious("0xdev1...")

# Check if project is safe
is_safe, warnings = tracker.is_project_safe("0x123...")
```

**Reputation Scoring:**
- Starts at 50/100
- -30 points for rug pulls
- -25 points for scams
- Tracks across all projects
- Warnings displayed to users

**Data Storage:**
- Saved to `dev_reputation_data.json`
- Persistent across bot restarts
- Can be backed up and shared

### 3. 📱 Social Media Alerts

Automatically post alerts about suspicious tokens and opportunities to Twitter and integrate with other bots.

**Twitter Integration:**

Setup Twitter API credentials:
```bash
# .env file
TWITTER_API_KEY="your_api_key"
TWITTER_API_SECRET="your_api_secret"
TWITTER_ACCESS_TOKEN="your_access_token"
TWITTER_ACCESS_SECRET="your_access_secret"
```

Configuration:
```json
"social_media": {
  "enabled": true,
  "twitter_enabled": true,
  "min_risk_score": 70,
  "alert_on_rug_pull": true,
  "alert_on_high_potential": true
}
```

**Alert Types:**

1. **Rug Pull Alerts** 🛑
   ```
   🛑 RUG PULL ALERT 🛑
   
   Token: ScamToken (0x123...)
   Developer: 0xdev...
   Severity: CRITICAL
   
   Developer sold 50% of holdings
   
   #RugPull #CryptoScam #DeFi #Warning
   ```

2. **Suspicious Token Alerts** ⚠️
   ```
   ⚠️ SUSPICIOUS TOKEN DETECTED
   
   Token: ShadyToken (0x456...)
   Risk Score: 85/100
   
   Red Flags:
   • Developer has 2 previous rug pulls
   • Abnormal token distribution
   • Hidden mint function
   
   🔍 Do your own research!
   
   #CryptoWarning #DeFi #DYOR
   ```

3. **High Potential Alerts** 🚀
   ```
   🚀 HIGH POTENTIAL TOKEN DETECTED
   
   Token: GemToken (0x789...)
   Potential Score: 88/100
   
   Why it looks good:
   ✅ Excellent liquidity: 50 ETH
   ✅ Verified contract
   ✅ Experienced developer
   
   ⚠️ Not financial advice! DYOR!
   
   #Crypto #DeFi #Gem
   ```

### 4. 🤖 Overseer Bot Integration

Connect with atomicfizzcaps.xyz overseer-bot-ai for cross-platform alerts and coordination.

**Setup:**
```bash
# .env file
OVERSEER_WEBHOOK_URL="https://your-overseer-bot.com/webhook"
OVERSEER_API_KEY="your_api_key"
```

Configuration:
```json
"social_media": {
  "overseer_bot_enabled": true,
  "overseer_webhook_url": "",  // Loaded from .env
  "overseer_api_key": ""       // Loaded from .env
}
```

**How It Works:**
- Bot sends JSON alerts to overseer webhook
- Includes full alert data (type, severity, token info, analysis)
- Overseer can process and redistribute alerts
- Bi-directional communication possible

**Alert Data Structure:**
```json
{
  "type": "rug_pull_alert",
  "severity": "critical",
  "token_address": "0x123...",
  "token_name": "ScamToken",
  "dev_address": "0xdev...",
  "details": "Developer sold 50% of holdings",
  "message": "Full formatted message",
  "timestamp": "2026-02-10T12:00:00"
}
```

### 5. 🎯 Token Opportunity Scorer

Advanced multi-factor scoring system to identify "ape-worthy" tokens.

**Scoring Factors:**
1. **Liquidity (20%)** - Pool depth and stability
2. **Safety (25%)** - Honeypot checks, taxes, contract verification
3. **Developer (20%)** - Reputation and history
4. **Sentiment (15%)** - AI sentiment analysis
5. **Technical (10%)** - Holder count, contract age
6. **Community (10%)** - Social metrics (future)

**Configuration:**
```json
"opportunity_scorer": {
  "enabled": true,
  "weight_liquidity": 20,
  "weight_safety": 25,
  "weight_developer": 20,
  "weight_sentiment": 15,
  "weight_technical": 10,
  "weight_community": 10,
  "min_score_for_alert": 75,
  "excellent_score": 85
}
```

**Score Interpretation:**
- **85-100**: 🌟 Excellent - Strong buy signal
- **75-84**: ✅ Good - Consider buying
- **60-74**: 👌 Moderate - Proceed with caution
- **40-59**: ⚠️ Low - Not recommended
- **0-39**: ❌ Poor - Avoid

**Usage:**
```python
from token_opportunity_scorer import TokenOpportunityScorer

scorer = TokenOpportunityScorer(config)

score, details = scorer.score_token(
    token_data=token_info,
    safety_results=safety_check,
    dev_reputation=dev_info,
    ai_analysis=ai_results
)

is_worthy, score, reasons = scorer.is_ape_worthy(
    token_data, safety_results, dev_reputation, ai_analysis
)
```

## Complete Integration Example

```python
from enhanced_bot_orchestrator import EnhancedBotOrchestrator

# Initialize with your bot
orchestrator = EnhancedBotOrchestrator(bot_instance, config)

# Start dashboard
orchestrator.start_dashboard()

# Analyze a token with all features
results = orchestrator.analyze_token_enhanced(
    token_address="0x123...",
    token_name="NewToken",
    safety_results=safety_check_results
)

print(f"Opportunity Score: {results['opportunity_score']}/100")
print(f"Ape Worthy: {results['is_ape_worthy']}")
print(f"Developer Safe: {results['project_safe']}")
print(f"Warnings: {results['warnings']}")

# Record events
orchestrator.record_rug_pull("0x123...", "ScamToken", "0xdev...", "critical", "Details")
orchestrator.record_dev_sell("0x123...", "0xdev...", 30.0, "Sold 30%")
orchestrator.record_successful_trade("0x789...", 150.50)

# Get statistics
stats = orchestrator.get_statistics()
```

## Quick Start Guide

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Features
Edit `config.json`:
```json
{
  "dashboard": {"enabled": true, "port": 5000},
  "social_media": {"enabled": true, "twitter_enabled": true},
  "opportunity_scorer": {"enabled": true}
}
```

### Step 3: Add API Keys
Edit `.env`:
```bash
# Twitter (optional)
TWITTER_API_KEY="your_key"
TWITTER_API_SECRET="your_secret"
TWITTER_ACCESS_TOKEN="your_token"
TWITTER_ACCESS_SECRET="your_token_secret"

# Overseer Bot (optional)
OVERSEER_WEBHOOK_URL="https://your-bot.com/webhook"
OVERSEER_API_KEY="your_key"
```

### Step 4: Run
```python
from enhanced_bot_orchestrator import EnhancedBotOrchestrator

# Your existing bot setup...

# Add orchestrator
orchestrator = EnhancedBotOrchestrator(bot, config)
orchestrator.start_dashboard()

# Dashboard now available at http://127.0.0.1:5000
```

## Security Considerations

**API Keys:**
- Store all API keys in `.env` file
- Never commit `.env` to version control
- `.env` is already in `.gitignore`
- Use separate API keys for testing vs production

**Dashboard Access:**
- Default `127.0.0.1` = localhost only (secure)
- Change to `0.0.0.0` for external access (less secure)
- Consider adding authentication for production
- Use reverse proxy (nginx) for HTTPS in production

**Data Storage:**
- `dev_reputation_data.json` contains developer tracking
- Backup regularly
- Can contain sensitive analysis data
- Don't share publicly without sanitizing

## Troubleshooting

**Dashboard won't start:**
- Check if port 5000 is already in use
- Try different port in config
- Check firewall settings

**Twitter posts failing:**
- Verify API credentials in `.env`
- Check Twitter API access level
- Ensure OAuth 1.0a permissions

**Overseer webhook errors:**
- Verify webhook URL is accessible
- Check API key if required
- Review overseer bot logs

**Developer tracking not working:**
- Check file permissions for `dev_reputation_data.json`
- Verify JSON file is valid
- Check logs for errors

## Future Enhancements

Planned features:
- [ ] Telegram integration
- [ ] Discord webhooks
- [ ] Advanced community metrics
- [ ] Machine learning developer behavior
- [ ] Cross-chain developer tracking
- [ ] Dashboard authentication
- [ ] Historical analytics charts
- [ ] Export reports (PDF/CSV)
- [ ] Mobile app integration

## Contributing

Have ideas for new monitoring features? Open an issue or submit a PR!

## Support

For questions or issues:
- Check logs: `scalper_bot.log`
- Review dashboard console
- Open GitHub issue
- Check existing documentation

---

**Remember**: These features enhance safety and visibility but don't guarantee profits. Always DYOR (Do Your Own Research) and never invest more than you can afford to lose.
