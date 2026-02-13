"""
WSGI entry point for production deployment
Provides the Flask app instance for WSGI servers like Gunicorn

Note: The Flask app (monitoring_dashboard) is configured via environment variables.
Config files are optional and primarily used when running the full bot locally.
"""

import logging
import os
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Flask app with error handling
try:
    from monitoring_dashboard import app
except ImportError as e:
    logger.error(f"Failed to import monitoring_dashboard: {e}")
    logger.error("Ensure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)

logger.info("WSGI application initialized for production deployment")

# Export the Flask app for Gunicorn
application = app

if __name__ == '__main__':
    # For development/testing only - use Gunicorn in production
    port = int(os.getenv('PORT', 5000))
    logger.warning("Running Flask development server - use Gunicorn for production")
    app.run(host='0.0.0.0', port=port, debug=False)
