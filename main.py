"""
Main CLI entry point for Token Scalper Bot
"""

import argparse
import logging
import multiprocessing
import os
import sys
from scalper_bot import TokenScalper
from wallet_generator import main as wallet_gen_main
from airdrop_finder import AirdropFinder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default configuration file path
DEFAULT_CONFIG_PATH = 'config.json'

def run_bot(config_path):
    bot = TokenScalper(config_path)
    bot.run()

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
    logger.info("🚀 Starting Token Scalper Bot in web service mode")
    logger.info("📊 Dashboard will be available for monitoring")
    
    # Determine port from environment or default
    port = int(os.getenv('PORT', 5000))
    
    # Check if we should use Gunicorn (production) or Flask dev server (development)
    # Accepts true/1/yes (case insensitive) for enabled, anything else for disabled
    use_gunicorn_env = os.getenv('USE_GUNICORN', 'true').lower()
    use_gunicorn = use_gunicorn_env in ('true', '1', 'yes')
    
    if use_gunicorn:
        logger.info("🔧 Using Gunicorn production WSGI server")
        
        # Calculate number of workers (2 * CPU cores + 1, or 2 if CPU count unknown)
        try:
            workers = (2 * multiprocessing.cpu_count()) + 1
        except NotImplementedError:
            workers = 2
        
        # Limit workers based on available resources
        # WEB_CONCURRENCY is set by platforms like Render and Heroku
        web_concurrency = os.getenv('WEB_CONCURRENCY')
        if web_concurrency is not None:
            try:
                workers = min(workers, int(web_concurrency))
            except ValueError:
                logger.warning(f"Invalid WEB_CONCURRENCY value: {web_concurrency}, using calculated value: {workers}")
        
        # Timeout for worker processes (configurable)
        # Default timeout of 120 seconds to handle long-running requests
        # such as blockchain RPC calls, database queries, or AI analysis
        timeout = 120
        timeout_env = os.getenv('GUNICORN_TIMEOUT')
        if timeout_env is not None:
            try:
                timeout = int(timeout_env)
            except ValueError:
                logger.warning(f"Invalid GUNICORN_TIMEOUT value: {timeout_env}, using default: {timeout}")
        
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
        
        # Set config path in environment for wsgi.py (though not currently used)
        os.environ['CONFIG_PATH'] = config_path
        
        # Execute Gunicorn, replacing the current process
        # This allows Gunicorn to handle its own signal management and process control
        # The process will not return unless Gunicorn fails to start
        try:
            os.execvp('gunicorn', gunicorn_cmd)
        except (OSError, FileNotFoundError) as e:
            # OSError: Permission denied, invalid arguments, etc.
            # FileNotFoundError: gunicorn not found in PATH
            logger.error(f"Failed to start Gunicorn: {e}")
            logger.error("Ensure Gunicorn is installed: pip install gunicorn")
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
            # Intentionally catch all exceptions to ensure dashboard always starts
            # Config loading can fail for many reasons (file not found, invalid JSON,
            # missing keys, import errors, etc.) and we want the dashboard to be
            # available for monitoring even when the config is broken
            logger.warning(f"Could not load config from {config_path}: {e}")
            logger.info("Using minimal dashboard-only configuration")
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
    parser.add_argument('--config', type=str, default=DEFAULT_CONFIG_PATH, help='Path to config file')
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
