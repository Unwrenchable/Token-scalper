"""
Enhanced Bot Orchestrator with Monitoring, Social Media, and Developer Tracking
Integrates all new features into the main bot
"""

import logging
import threading
from typing import Dict, List, Optional
from datetime import datetime

from dev_reputation_tracker import DevReputationTracker
from social_media_alerts import SocialMediaAlerts
from monitoring_dashboard import MonitoringDashboard, dashboard_state
from token_opportunity_scorer import TokenOpportunityScorer

logger = logging.getLogger(__name__)


class EnhancedBotOrchestrator:
    """
    Enhanced bot orchestrator that integrates:
    - Developer reputation tracking
    - Social media alerts
    - Monitoring dashboard
    - Token opportunity scoring
    """
    
    def __init__(self, bot_instance, config: Dict):
        """
        Initialize enhanced orchestrator
        
        Args:
            bot_instance: Main scalper bot instance
            config: Configuration dictionary
        """
        self.bot = bot_instance
        self.config = config
        
        # Initialize new modules
        self.dev_tracker = DevReputationTracker()
        self.social_alerts = SocialMediaAlerts(config)
        self.opportunity_scorer = TokenOpportunityScorer(config)
        self.dashboard = MonitoringDashboard(config, self.dev_tracker, self.social_alerts)
        
        # Dashboard thread
        self.dashboard_thread = None
        
        logger.info("🚀 Enhanced Bot Orchestrator initialized")
        logger.info(f"   - Developer Tracking: {'✅' if self.dev_tracker else '❌'}")
        logger.info(f"   - Social Alerts: {'✅' if self.social_alerts.enabled else '❌'}")
        logger.info(f"   - Opportunity Scorer: {'✅' if self.opportunity_scorer.enabled else '❌'}")
        logger.info(f"   - Dashboard: {'✅' if self.dashboard.enabled else '❌'}")
    
    def start_dashboard(self):
        """Start the monitoring dashboard in a separate thread"""
        if not self.dashboard.enabled:
            logger.info("Dashboard is disabled")
            return
        
        def run_dashboard():
            try:
                self.dashboard.run()
            except Exception as e:
                logger.error(f"Dashboard error: {e}")
        
        self.dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
        self.dashboard_thread.start()
        logger.info("📊 Dashboard thread started")
    
    def analyze_token_enhanced(self, token_address: str, token_name: str, 
                               safety_results: Dict) -> Dict:
        """
        Enhanced token analysis with all new features
        
        Args:
            token_address: Token contract address
            token_name: Token name
            safety_results: Results from safety checker
            
        Returns:
            Enhanced analysis results
        """
        logger.info(f"🔍 Enhanced analysis for {token_name}")
        
        # Identify developers
        dev_addresses = self._identify_developers(token_address)
        
        # Get developer reputation
        dev_reputation = None
        if dev_addresses:
            dev_address = dev_addresses[0]  # Primary dev
            dev_reputation = self.dev_tracker.get_developer_reputation(dev_address)
            
            # Register if unknown
            if not dev_reputation:
                self.dev_tracker.register_developer(dev_address, token_address)
                self.dev_tracker.register_project(token_address, token_name, dev_addresses)
                dev_reputation = self.dev_tracker.get_developer_reputation(dev_address)
        
        # Check if project/devs are safe
        is_safe, warnings = self.dev_tracker.is_project_safe(token_address)
        
        # Score opportunity
        token_data = {'address': token_address, 'name': token_name}
        ai_analysis = safety_results if 'ai_risk_score' in safety_results else None
        
        score, details = self.opportunity_scorer.score_token(
            token_data, safety_results, dev_reputation, ai_analysis
        )
        
        # Check for alerts
        self._check_and_send_alerts(token_address, token_name, safety_results, 
                                   dev_reputation, score, details, warnings)
        
        # Update dashboard
        self._update_dashboard_data(token_address, token_name, score, details)
        
        return {
            'token_address': token_address,
            'token_name': token_name,
            'opportunity_score': score,
            'is_ape_worthy': details['is_ape_worthy'],
            'developer_reputation': dev_reputation,
            'project_safe': is_safe,
            'warnings': warnings,
            'details': details,
            'safety_results': safety_results
        }
    
    def record_rug_pull(self, token_address: str, token_name: str, 
                       dev_address: str, severity: str, details: str):
        """
        Record a rug pull event
        
        Args:
            token_address: Token contract address
            token_name: Token name
            dev_address: Developer wallet address
            severity: Severity level
            details: Details about the rug pull
        """
        logger.warning(f"🚨 Rug pull detected: {token_name}")
        
        # Flag in reputation tracker
        self.dev_tracker.flag_project(token_address, 'rug_pull', details)
        
        # Send social media alert
        if self.social_alerts.enabled:
            self.social_alerts.post_rug_pull_alert(
                token_address, token_name, dev_address, severity, details
            )
        
        # Update dashboard
        self.dashboard.add_alert('rug_pull', f"Rug pull: {token_name}", 'danger')
        
        # Update analytics
        stats = dashboard_state['analytics']
        stats['rug_pulls_avoided'] = stats.get('rug_pulls_avoided', 0) + 1
        self.dashboard.update_analytics(stats)
    
    def record_dev_sell(self, token_address: str, dev_address: str, 
                       amount_percent: float, details: str):
        """
        Record a developer selling event
        
        Args:
            token_address: Token contract address
            dev_address: Developer wallet address
            amount_percent: Percentage of holdings sold
            details: Additional details
        """
        logger.warning(f"⚠️ Dev sell detected: {amount_percent}% on {token_address}")
        
        # Record in reputation tracker
        self.dev_tracker.record_dev_sell_event(token_address, dev_address, 
                                               amount_percent, details)
        
        # Alert if significant
        if amount_percent >= 15:
            self.dashboard.add_alert('dev_sell', 
                                   f"Developer sold {amount_percent}% of {token_address}", 
                                   'warning')
    
    def record_successful_trade(self, token_address: str, profit_usd: float):
        """Record a successful trade"""
        stats = dashboard_state['analytics']
        stats['total_trades'] = stats.get('total_trades', 0) + 1
        stats['successful_trades'] = stats.get('successful_trades', 0) + 1
        stats['total_profit_usd'] = stats.get('total_profit_usd', 0) + profit_usd
        self.dashboard.update_analytics(stats)
    
    def _identify_developers(self, token_address: str) -> List[str]:
        """
        Identify developer wallets for a token
        Uses wallet monitor or blockchain analysis
        """
        # This would integrate with wallet_monitor.py
        # For now, return empty list
        return []
    
    def _check_and_send_alerts(self, token_address: str, token_name: str,
                               safety_results: Dict, dev_reputation: Optional[Dict],
                               score: int, details: Dict, warnings: List[str]):
        """Check conditions and send appropriate alerts"""
        
        # High-risk alert
        if 'ai_risk_score' in safety_results:
            risk_score = safety_results['ai_risk_score']
            if risk_score >= self.social_alerts.min_risk_score_for_alert:
                self.social_alerts.post_suspicious_token_alert(
                    token_address, token_name, risk_score, warnings
                )
                self.dashboard.add_alert('suspicious_token',
                                       f"High risk token: {token_name} (risk: {risk_score})",
                                       'warning')
        
        # High potential alert
        if details['is_ape_worthy'] and self.social_alerts.alert_on_high_potential:
            self.social_alerts.post_high_potential_alert(
                token_address, token_name, score, details['reasons']
            )
            self.dashboard.add_alert('high_potential',
                                   f"High potential token: {token_name} (score: {score})",
                                   'success')
        
        # Developer warnings
        if warnings and dev_reputation:
            if dev_reputation.get('rug_pull_count', 0) > 0:
                self.dashboard.add_alert('dev_warning',
                                       f"Developer has rug pull history: {token_name}",
                                       'danger')
    
    def _update_dashboard_data(self, token_address: str, token_name: str,
                              score: int, details: Dict):
        """Update dashboard with new data"""
        
        # Update developer stats
        dev_stats = self.dev_tracker.get_statistics()
        self.dashboard.update_developer_stats(dev_stats)
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            'developer_tracking': self.dev_tracker.get_statistics(),
            'analytics': dashboard_state['analytics'],
            'social_alerts_enabled': self.social_alerts.enabled,
            'dashboard_enabled': self.dashboard.enabled
        }
