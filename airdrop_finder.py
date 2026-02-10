"""
Airdrop Finder Module
Finds and filters airdrop opportunities from public sources.
"""

import requests
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class AirdropFinder:
    """Finds airdrop opportunities from aggregators/APIs"""

    AGGREGATORS = [
        'https://api.airdrops.io/airdrops',
        # Add more APIs or sources as needed
    ]

    @staticmethod
    def fetch_airdrops() -> List[Dict]:
        """Fetch airdrop opportunities from known sources"""
        results = []
        for url in AirdropFinder.AGGREGATORS:
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    # Normalize data if needed
                    if isinstance(data, dict) and 'airdrops' in data:
                        results.extend(data['airdrops'])
                    elif isinstance(data, list):
                        results.extend(data)
                else:
                    logger.warning(f"Failed to fetch from {url}: {resp.status_code}")
            except Exception as e:
                logger.warning(f"Error fetching from {url}: {e}")
        return results

    @staticmethod
    def filter_good_airdrops(airdrops: List[Dict]) -> List[Dict]:
        """Filter for reputable, active, non-scam airdrops"""
        good = []
        for a in airdrops:
            # Example criteria: not expired, has website, not flagged as scam
            if a.get('status', '').lower() == 'active' and a.get('website') and not a.get('scam', False):
                good.append(a)
        return good

    @staticmethod
    def get_good_airdrops() -> List[Dict]:
        """Fetch and filter good airdrops"""
        all_airdrops = AirdropFinder.fetch_airdrops()
        return AirdropFinder.filter_good_airdrops(all_airdrops)
