"""
WSGI entry point for production deployment
Provides the Flask app instance for WSGI servers like Gunicorn
"""

import logging
import os
import json
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default configuration file path
DEFAULT_CONFIG_PATH = 'config.json'

# Import Flask app with error handling
try:
    from monitoring_dashboard import app
    from config_loader import ConfigLoader
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    logger.error("Ensure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)

# Load configuration
config_path = os.getenv('CONFIG_PATH', DEFAULT_CONFIG_PATH)
try:
    config = ConfigLoader.load_config(config_path)
except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
    # In production, config loading failures are acceptable for dashboard-only mode
    # The dashboard can run with minimal config using environment variables
    logger.warning(f"Could not load config from {config_path}: {e}")
    logger.info("Using minimal dashboard-only configuration")
    # Use minimal config for dashboard only
    config = {
        'dashboard': {
            'enabled': True,
            'host': '0.0.0.0',
            'port': int(os.getenv('PORT', 5000))
        }
    }

logger.info("WSGI application initialized")

# Export the Flask app for Gunicorn
application = app

if __name__ == '__main__':
    # For development/testing only
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
