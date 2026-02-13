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
    Uses Gunicorn in production for better performance and security.
    """
    import subprocess
    import sys
    
    logger.info("🚀 Starting Token Scalper Bot in web service mode")
    logger.info("📊 Dashboard will be available for monitoring")
    
    # Determine port from environment or default
    port = int(os.getenv('PORT', 5000))
    
    # Check if we should use Gunicorn (production) or Flask dev server (development)
    use_gunicorn = os.getenv('USE_GUNICORN', 'true').lower() in ('true', '1', 'yes')
    
    if use_gunicorn:
        logger.info("🔧 Using Gunicorn production WSGI server")
        
        # Calculate number of workers (2 * CPU cores + 1, or 2 if CPU count unknown)
        try:
            import multiprocessing
            workers = (2 * multiprocessing.cpu_count()) + 1
        except (NotImplementedError, ValueError):
            workers = 2
        
        # Limit workers based on available resources
        # WEB_CONCURRENCY is set by platforms like Render and Heroku
        web_concurrency = os.getenv('WEB_CONCURRENCY')
        if web_concurrency is not None:
            workers = min(workers, int(web_concurrency))
        
        # Timeout for worker processes (configurable)
        timeout = int(os.getenv('GUNICORN_TIMEOUT', '120'))
        
        # Gunicorn command
        gunicorn_cmd = [
            'gunicorn',
            '--bind', f'0.0.0.0:{port}',
            '--workers', str(workers),
            '--timeout', str(timeout),
            '--access-logfile', '-',
            '--error-logfile', '-',
            '--log-level', 'info',
            'wsgi:application'
        ]
        
        logger.info(f"Starting Gunicorn with {workers} workers on port {port}")
        
        # Set config path in environment for wsgi.py
        os.environ['CONFIG_PATH'] = config_path
        
        # Run Gunicorn
        try:
            subprocess.run(gunicorn_cmd, check=True)
        except KeyboardInterrupt:
            logger.info("Shutting down gracefully...")
        except subprocess.CalledProcessError as e:
            logger.error(f"Gunicorn failed: {e}")
            sys.exit(1)
    else:
        # Fall back to Flask development server
        logger.warning("⚠️  Using Flask development server (not recommended for production)")
        logger.warning("Set USE_GUNICORN=true environment variable to use production server")
        
        from monitoring_dashboard import MonitoringDashboard
        from config_loader import ConfigLoader
        
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
                    'port': port
                }
            }
        
        # Ensure dashboard is enabled for web service mode
        if 'dashboard' not in config:
            config['dashboard'] = {}
        config['dashboard']['enabled'] = True
        config['dashboard']['host'] = '0.0.0.0'  # Bind to all interfaces
        config['dashboard']['port'] = port
        
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
