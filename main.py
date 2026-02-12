"""
Main CLI entry point for Token Scalper Bot
"""

import argparse
import logging
import os
import sys
from scalper_bot import TokenScalper
from wallet_generator import main as wallet_gen_main
from airdrop_finder import AirdropFinder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_bot(config_path):
    bot = TokenScalper(config_path)
    bot.search_and_participate_airdrops()
    # You can add more bot actions here (e.g., start trading loop)

def search_airdrops():
    finder = AirdropFinder()
    airdrops = finder.get_good_airdrops()
    for a in airdrops:
        print(f"{a.get('title', a.get('name', 'unknown'))}: {a.get('website')}")
    print(f"Total good airdrops found: {len(airdrops)}")

def generate_wallets():
    wallet_gen_main()

def run_web_service(config_path):
    """
    Run the bot as a web service with dashboard
    This is used when deployed to platforms like Render, Heroku, etc.
    """
    from monitoring_dashboard import MonitoringDashboard
    from config_loader import ConfigLoader
    
    logger.info("🚀 Starting Token Scalper Bot in web service mode")
    logger.info("📊 Dashboard will be available for monitoring")
    
    # Load config
    try:
        config = ConfigLoader.load_config(config_path)
    except Exception as e:
        logger.warning(f"Could not load config from {config_path}: {e}")
        # Use minimal config for dashboard only
        config = {
            'dashboard': {
                'enabled': True,
                'host': '0.0.0.0',
                'port': int(os.getenv('PORT', 5000))
            }
        }
    
    # Ensure dashboard is enabled for web service mode
    if 'dashboard' not in config:
        config['dashboard'] = {}
    config['dashboard']['enabled'] = True
    config['dashboard']['host'] = '0.0.0.0'  # Bind to all interfaces
    config['dashboard']['port'] = int(os.getenv('PORT', config.get('dashboard', {}).get('port', 5000)))
    
    # Initialize and run dashboard
    dashboard = MonitoringDashboard(config)
    dashboard.run()

def main():
    parser = argparse.ArgumentParser(description="Token Scalper Bot CLI")
    parser.add_argument('--config', type=str, default='config.json', help='Path to config file')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('run', help='Run the scalper bot')
    subparsers.add_parser('airdrops', help='Search for good airdrop opportunities')
    subparsers.add_parser('genwallets', help='Generate wallets and export to .env')
    subparsers.add_parser('web', help='Run as web service with dashboard (for deployment)')

    args = parser.parse_args()

    if args.command == 'run':
        run_bot(args.config)
    elif args.command == 'airdrops':
        search_airdrops()
    elif args.command == 'genwallets':
        generate_wallets()
    elif args.command == 'web':
        run_web_service(args.config)
    else:
        # If no command provided and PORT env var exists, assume web service deployment
        if os.getenv('PORT'):
            logger.info("Detected PORT environment variable - running in web service mode")
            run_web_service(args.config)
        else:
            parser.print_help()

if __name__ == '__main__':
    main()
