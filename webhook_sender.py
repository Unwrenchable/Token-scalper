"""
Webhook sender module for Token-scalper
Sends alerts to configured endpoints (Twitter bot, UI dashboard, etc.)
"""

import os
import requests
import logging

logger = logging.getLogger(__name__)

# Load webhook URLs and API key from environment
WEBHOOK_URLS = os.getenv("WEBHOOK_URLS", "").split(",")
WEBHOOK_API_KEY = os.getenv("WEBHOOK_API_KEY", "")


def send_alert_to_webhooks(alert: dict):
    """
    Send alert to all configured webhook endpoints.
    Args:
        alert (dict): Alert payload (should match agreed schema)
    """
    if not WEBHOOK_URLS or not WEBHOOK_API_KEY:
        logger.warning("No webhook URLs or API key configured. Skipping alert send.")
        return
    for url in WEBHOOK_URLS:
        url = url.strip()
        if not url:
            continue
        try:
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": WEBHOOK_API_KEY
            }
            resp = requests.post(url, json=alert, headers=headers, timeout=10)
            resp.raise_for_status()
            logger.info(f"✅ Alert sent to {url}")
        except Exception as e:
            logger.error(f"❌ Failed to send alert to {url}: {e}")
