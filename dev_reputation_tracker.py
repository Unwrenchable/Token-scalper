"""
Developer Reputation Tracker
Tracks developer wallets across projects and builds reputation scores
"""

import json
import logging
from typing import Dict, List, Optional, Set
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class DevReputationTracker:
    """
    Tracks developer reputation across multiple projects
    Identifies patterns of scam behavior and links projects to known bad actors
    """
    
    def __init__(self, data_file: str = 'dev_reputation_data.json'):
        """
        Initialize developer reputation tracker
        
        Args:
            data_file: Path to JSON file for storing reputation data
        """
        self.data_file = data_file
        self.data = self._load_data()
        
    def _load_data(self) -> Dict:
        """Load reputation data from file"""
        try:
            if Path(self.data_file).exists():
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                logger.info(f"Loaded reputation data for {len(data.get('developers', {}))} developers")
                return data
        except Exception as e:
            logger.error(f"Error loading reputation data: {e}")
        
        # Default structure
        return {
            'developers': {},  # address -> dev info
            'projects': {},    # token_address -> project info
            'scam_patterns': [],  # list of identified scam patterns
            'last_updated': datetime.now().isoformat()
        }
    
    def _save_data(self):
        """Save reputation data to file"""
        try:
            self.data['last_updated'] = datetime.now().isoformat()
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
            logger.info("Reputation data saved successfully")
        except Exception as e:
            logger.error(f"Error saving reputation data: {e}")
    
    def register_developer(self, dev_address: str, token_address: str, 
                          initial_reputation: int = 50) -> None:
        """
        Register a developer for a token
        
        Args:
            dev_address: Developer wallet address
            token_address: Token contract address
            initial_reputation: Starting reputation score (0-100)
        """
        dev_address = dev_address.lower()
        token_address = token_address.lower()
        
        if dev_address not in self.data['developers']:
            self.data['developers'][dev_address] = {
                'address': dev_address,
                'reputation_score': initial_reputation,
                'projects': [],
                'scam_count': 0,
                'rug_pull_count': 0,
                'successful_projects': 0,
                'flags': [],
                'first_seen': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat()
            }
            logger.info(f"Registered new developer: {dev_address}")
        
        # Add project to developer's portfolio
        if token_address not in self.data['developers'][dev_address]['projects']:
            self.data['developers'][dev_address]['projects'].append(token_address)
            self.data['developers'][dev_address]['last_activity'] = datetime.now().isoformat()
        
        self._save_data()
    
    def register_project(self, token_address: str, token_name: str,
                        dev_addresses: List[str], initial_risk: str = 'unknown') -> None:
        """
        Register a new project
        
        Args:
            token_address: Token contract address
            token_name: Name of the token
            dev_addresses: List of developer wallet addresses
            initial_risk: Risk level (safe, caution, high, critical, unknown)
        """
        token_address = token_address.lower()
        dev_addresses = [addr.lower() for addr in dev_addresses]
        
        self.data['projects'][token_address] = {
            'address': token_address,
            'name': token_name,
            'developers': dev_addresses,
            'risk_level': initial_risk,
            'status': 'active',  # active, rugged, abandoned, successful
            'created_at': datetime.now().isoformat(),
            'flags': [],
            'rug_pull_detected': False,
            'dev_sell_events': [],
            'community_reports': 0
        }
        
        # Register each developer
        for dev_addr in dev_addresses:
            self.register_developer(dev_addr, token_address)
        
        logger.info(f"Registered project: {token_name} ({token_address})")
        self._save_data()
    
    def flag_developer(self, dev_address: str, flag_type: str, reason: str) -> None:
        """
        Add a flag to a developer's record
        
        Args:
            dev_address: Developer wallet address
            flag_type: Type of flag (scam, rug_pull, suspicious, honeypot)
            reason: Description of the issue
        """
        dev_address = dev_address.lower()
        
        if dev_address in self.data['developers']:
            flag = {
                'type': flag_type,
                'reason': reason,
                'timestamp': datetime.now().isoformat()
            }
            self.data['developers'][dev_address]['flags'].append(flag)
            
            # Update counters
            if flag_type == 'rug_pull':
                self.data['developers'][dev_address]['rug_pull_count'] += 1
                self.data['developers'][dev_address]['reputation_score'] = max(0, 
                    self.data['developers'][dev_address]['reputation_score'] - 30)
            elif flag_type == 'scam':
                self.data['developers'][dev_address]['scam_count'] += 1
                self.data['developers'][dev_address]['reputation_score'] = max(0,
                    self.data['developers'][dev_address]['reputation_score'] - 25)
            
            logger.warning(f"Flagged developer {dev_address}: {flag_type} - {reason}")
            self._save_data()
    
    def flag_project(self, token_address: str, flag_type: str, reason: str) -> None:
        """
        Add a flag to a project and its developers
        
        Args:
            token_address: Token contract address
            flag_type: Type of flag
            reason: Description of the issue
        """
        token_address = token_address.lower()
        
        if token_address in self.data['projects']:
            flag = {
                'type': flag_type,
                'reason': reason,
                'timestamp': datetime.now().isoformat()
            }
            self.data['projects'][token_address]['flags'].append(flag)
            
            # Update project status
            if flag_type == 'rug_pull':
                self.data['projects'][token_address]['status'] = 'rugged'
                self.data['projects'][token_address]['rug_pull_detected'] = True
            
            # Flag all developers of this project
            for dev_addr in self.data['projects'][token_address]['developers']:
                self.flag_developer(dev_addr, flag_type, f"Project {token_address}: {reason}")
            
            logger.warning(f"Flagged project {token_address}: {flag_type} - {reason}")
            self._save_data()
    
    def record_dev_sell_event(self, token_address: str, dev_address: str, 
                             amount_percent: float, details: str) -> None:
        """
        Record a developer selling event
        
        Args:
            token_address: Token contract address
            dev_address: Developer wallet address
            amount_percent: Percentage of holdings sold
            details: Additional details about the sell
        """
        token_address = token_address.lower()
        dev_address = dev_address.lower()
        
        if token_address in self.data['projects']:
            event = {
                'dev_address': dev_address,
                'amount_percent': amount_percent,
                'details': details,
                'timestamp': datetime.now().isoformat()
            }
            self.data['projects'][token_address]['dev_sell_events'].append(event)
            
            # Check for rug pull threshold
            if amount_percent >= 30:
                self.flag_project(token_address, 'rug_pull', 
                                f"Developer sold {amount_percent}% of holdings")
            elif amount_percent >= 15:
                self.flag_project(token_address, 'suspicious',
                                f"Developer sold {amount_percent}% of holdings")
            
            self._save_data()
    
    def get_developer_reputation(self, dev_address: str) -> Optional[Dict]:
        """Get reputation info for a developer"""
        dev_address = dev_address.lower()
        return self.data['developers'].get(dev_address)
    
    def get_project_info(self, token_address: str) -> Optional[Dict]:
        """Get info for a project"""
        token_address = token_address.lower()
        return self.data['projects'].get(token_address)
    
    def get_developer_projects(self, dev_address: str) -> List[Dict]:
        """Get all projects associated with a developer"""
        dev_address = dev_address.lower()
        
        if dev_address not in self.data['developers']:
            return []
        
        project_addresses = self.data['developers'][dev_address]['projects']
        return [self.data['projects'][addr] for addr in project_addresses 
                if addr in self.data['projects']]
    
    def is_developer_suspicious(self, dev_address: str, threshold: int = 40) -> bool:
        """
        Check if a developer is suspicious based on reputation
        
        Args:
            dev_address: Developer wallet address
            threshold: Reputation threshold (below this is suspicious)
            
        Returns:
            True if developer is suspicious
        """
        dev_info = self.get_developer_reputation(dev_address)
        if not dev_info:
            return False
        
        return dev_info['reputation_score'] < threshold or \
               dev_info['rug_pull_count'] > 0 or \
               dev_info['scam_count'] > 1
    
    def is_project_safe(self, token_address: str) -> Tuple[bool, List[str]]:
        """
        Check if a project is safe based on developer reputation
        
        Args:
            token_address: Token contract address
            
        Returns:
            Tuple of (is_safe, list_of_warnings)
        """
        project_info = self.get_project_info(token_address)
        if not project_info:
            return True, []  # Unknown project, no data
        
        warnings = []
        
        # Check if already flagged as rugged
        if project_info['rug_pull_detected']:
            return False, ['Project has been rugged']
        
        # Check developers
        for dev_addr in project_info['developers']:
            dev_info = self.get_developer_reputation(dev_addr)
            if dev_info:
                if dev_info['rug_pull_count'] > 0:
                    warnings.append(f"Developer {dev_addr[:10]}... has {dev_info['rug_pull_count']} rug pulls")
                if dev_info['scam_count'] > 0:
                    warnings.append(f"Developer {dev_addr[:10]}... has {dev_info['scam_count']} scams")
                if dev_info['reputation_score'] < 30:
                    warnings.append(f"Developer {dev_addr[:10]}... has very low reputation ({dev_info['reputation_score']})")
        
        # Check for excessive dev selling
        total_dev_sell = sum(event['amount_percent'] for event in project_info['dev_sell_events'])
        if total_dev_sell > 50:
            warnings.append(f"Developers have sold {total_dev_sell}% of holdings")
        
        is_safe = len(warnings) == 0 or (len(warnings) == 1 and 'low reputation' in warnings[0])
        
        return is_safe, warnings
    
    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        total_devs = len(self.data['developers'])
        total_projects = len(self.data['projects'])
        
        scam_devs = sum(1 for dev in self.data['developers'].values() 
                       if dev['scam_count'] > 0 or dev['rug_pull_count'] > 0)
        
        rugged_projects = sum(1 for proj in self.data['projects'].values()
                             if proj['rug_pull_detected'])
        
        return {
            'total_developers': total_devs,
            'total_projects': total_projects,
            'scam_developers': scam_devs,
            'rugged_projects': rugged_projects,
            'tracking_since': self.data.get('last_updated', 'unknown')
        }
