#!/usr/bin/env python3
"""
Example: Using Monitoring Dashboard and Social Media Integration
Demonstrates how to integrate all new features into your bot
"""

import logging
from config_loader import load_config_with_env
from enhanced_bot_orchestrator import EnhancedBotOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Example of using enhanced bot features
    """
    # Load configuration
    logger.info("Loading configuration...")
    config = load_config_with_env('config.json')
    
    # For this example, we'll create a mock bot instance
    # In real usage, this would be your TokenScalper instance
    class MockBot:
        def __init__(self):
            self.active_positions = []
    
    bot = MockBot()
    
    # Initialize enhanced orchestrator
    logger.info("Initializing Enhanced Bot Orchestrator...")
    orchestrator = EnhancedBotOrchestrator(bot, config)
    
    # Start dashboard (in background thread)
    logger.info("Starting monitoring dashboard...")
    orchestrator.start_dashboard()
    logger.info("✅ Dashboard available at http://127.0.0.1:5000")
    
    # Example: Analyze a token with enhanced features
    logger.info("\n" + "="*60)
    logger.info("EXAMPLE: Enhanced Token Analysis")
    logger.info("="*60)
    
    # Mock token data
    token_address = "0x1234567890abcdef1234567890abcdef12345678"
    token_name = "ExampleToken"
    
    # Mock safety results (would come from safety_checker in real bot)
    safety_results = {
        'safe': True,
        'is_honeypot': False,
        'liquidity_eth': 25.5,
        'buy_tax': 3.0,
        'sell_tax': 3.0,
        'contract_verified': True,
        'holder_count': 250,
        'contract_age': 3600 * 24 * 2,  # 2 days
        'ai_risk_score': 35,  # Low risk
        'ai_sentiment_score': 72  # Positive sentiment
    }
    
    # Perform enhanced analysis
    logger.info(f"\nAnalyzing token: {token_name}")
    results = orchestrator.analyze_token_enhanced(
        token_address=token_address,
        token_name=token_name,
        safety_results=safety_results
    )
    
    # Display results
    logger.info(f"\n📊 ANALYSIS RESULTS:")
    logger.info(f"   Opportunity Score: {results['opportunity_score']}/100")
    logger.info(f"   Ape Worthy: {'✅ YES' if results['is_ape_worthy'] else '❌ NO'}")
    logger.info(f"   Project Safe: {'✅ YES' if results['project_safe'] else '❌ NO'}")
    
    if results['warnings']:
        logger.warning(f"   Warnings: {', '.join(results['warnings'])}")
    
    logger.info(f"   Rating: {results['details']['rating_emoji']} {results['details']['rating']}")
    
    if results['details']['reasons']:
        logger.info(f"\n   Positive Indicators:")
        for reason in results['details']['reasons']:
            logger.info(f"      • {reason}")
    
    # Example: Record various events
    logger.info("\n" + "="*60)
    logger.info("EXAMPLE: Recording Events")
    logger.info("="*60)
    
    # Record a successful trade
    logger.info("\n📈 Recording successful trade...")
    orchestrator.record_successful_trade(token_address, profit_usd=125.50)
    
    # Example: Detect and report rug pull
    logger.info("\n🚨 Example: Detecting rug pull...")
    scam_token = "0xabcdef1234567890abcdef1234567890abcdef12"
    scam_dev = "0xbaddeveloper123456789012345678901234567890"
    
    orchestrator.record_rug_pull(
        token_address=scam_token,
        token_name="ScamToken",
        dev_address=scam_dev,
        severity="critical",
        details="Developer sold 60% of holdings in single transaction"
    )
    
    # Example: Record dev sell event
    logger.info("\n⚠️ Example: Recording developer sell event...")
    orchestrator.record_dev_sell(
        token_address=token_address,
        dev_address=scam_dev,
        amount_percent=18.5,
        details="Developer sold 18.5% gradually over 2 hours"
    )
    
    # Get and display statistics
    logger.info("\n" + "="*60)
    logger.info("STATISTICS")
    logger.info("="*60)
    
    stats = orchestrator.get_statistics()
    
    logger.info(f"\n📊 Analytics:")
    logger.info(f"   Total Trades: {stats['analytics'].get('total_trades', 0)}")
    logger.info(f"   Successful Trades: {stats['analytics'].get('successful_trades', 0)}")
    logger.info(f"   Rug Pulls Avoided: {stats['analytics'].get('rug_pulls_avoided', 0)}")
    logger.info(f"   Total Profit: ${stats['analytics'].get('total_profit_usd', 0):.2f}")
    
    logger.info(f"\n👥 Developer Tracking:")
    dev_stats = stats['developer_tracking']
    logger.info(f"   Tracked Developers: {dev_stats['total_developers']}")
    logger.info(f"   Flagged Developers: {dev_stats['scam_developers']}")
    logger.info(f"   Tracked Projects: {dev_stats['total_projects']}")
    logger.info(f"   Rugged Projects: {dev_stats['rugged_projects']}")
    
    logger.info(f"\n🔧 Feature Status:")
    logger.info(f"   Social Alerts: {'✅ Enabled' if stats['social_alerts_enabled'] else '❌ Disabled'}")
    logger.info(f"   Dashboard: {'✅ Enabled' if stats['dashboard_enabled'] else '❌ Disabled'}")
    
    # Keep running for dashboard access
    logger.info("\n" + "="*60)
    logger.info("Dashboard is running. Access it at: http://127.0.0.1:5000")
    logger.info("Press Ctrl+C to stop")
    logger.info("="*60 + "\n")
    
    try:
        # Keep main thread alive for dashboard
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\n\nShutting down gracefully...")


if __name__ == '__main__':
    main()
