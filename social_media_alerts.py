"""
Social Media Alert Module
Handles posting alerts to Twitter and integration with overseer-bot-ai
"""

import logging
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class SocialMediaAlerts:
    """
    Manages social media alerts for suspicious tokens and rug pulls
    Integrates with Twitter API and overseer-bot-ai
    """
    
    def __init__(self, config: Dict):
        """
        Initialize social media alerts
        
        Args:
            config: Configuration dictionary with social media settings
        """
        self.config = config
        self.social_config = config.get('social_media', {})
        self.enabled = self.social_config.get('enabled', False)
        
        # Twitter configuration
        self.twitter_enabled = self.social_config.get('twitter_enabled', False)
        self.twitter_api_key = self.social_config.get('twitter_api_key', '')
        self.twitter_api_secret = self.social_config.get('twitter_api_secret', '')
        self.twitter_access_token = self.social_config.get('twitter_access_token', '')
        self.twitter_access_secret = self.social_config.get('twitter_access_secret', '')
        
        # Overseer bot integration
        self.overseer_enabled = self.social_config.get('overseer_bot_enabled', False)
        self.overseer_webhook_url = self.social_config.get('overseer_webhook_url', '')
        self.overseer_api_key = self.social_config.get('overseer_api_key', '')
        
        # Alert thresholds
        self.min_risk_score_for_alert = self.social_config.get('min_risk_score', 70)
        self.alert_on_rug_pull = self.social_config.get('alert_on_rug_pull', True)
        self.alert_on_high_potential = self.social_config.get('alert_on_high_potential', True)
        
        if self.enabled:
            logger.info("📱 Social Media Alerts initialized")
            if self.twitter_enabled:
                logger.info("🐦 Twitter integration enabled")
            if self.overseer_enabled:
                logger.info("🤖 Overseer bot integration enabled")
    
    def post_rug_pull_alert(self, token_address: str, token_name: str, 
                           dev_address: str, severity: str, details: str) -> bool:
        """
        Post a rug pull alert to social media
        
        Args:
            token_address: Token contract address
            token_name: Name of the token
            dev_address: Developer wallet address
            severity: Alert severity (low, medium, high, critical)
            details: Additional details about the rug pull
            
        Returns:
            True if alert was posted successfully
        """
        if not self.enabled or not self.alert_on_rug_pull:
            return False
        
        # Create alert message
        emoji_map = {
            'low': '⚠️',
            'medium': '🚨',
            'high': '🔴',
            'critical': '🛑'
        }
        emoji = emoji_map.get(severity, '⚠️')
        
        message = f"""{emoji} RUG PULL ALERT {emoji}

Token: {token_name} ({token_address[:10]}...)
Developer: {dev_address[:10]}...
Severity: {severity.upper()}

{details}

#RugPull #CryptoScam #DeFi #Warning"""
        
        success = True
        
        # Post to Twitter
        if self.twitter_enabled:
            success = success and self._post_to_twitter(message)
        
        # Send to Overseer bot
        if self.overseer_enabled:
            alert_data = {
                'type': 'rug_pull_alert',
                'severity': severity,
                'token_address': token_address,
                'token_name': token_name,
                'dev_address': dev_address,
                'details': details,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            success = success and self._send_to_overseer(alert_data)
        
        if success:
            logger.info(f"🔔 Posted rug pull alert for {token_name}")
        
        return success
    
    def post_suspicious_token_alert(self, token_address: str, token_name: str,
                                   risk_score: int, warnings: List[str]) -> bool:
        """
        Post an alert about a suspicious token
        
        Args:
            token_address: Token contract address
            token_name: Name of the token
            risk_score: AI risk score (0-100)
            warnings: List of warning messages
            
        Returns:
            True if alert was posted successfully
        """
        if not self.enabled or risk_score < self.min_risk_score_for_alert:
            return False
        
        # Create alert message
        warning_text = '\n'.join([f"• {w}" for w in warnings[:3]])  # Limit to 3 warnings
        
        message = f"""⚠️ SUSPICIOUS TOKEN DETECTED

Token: {token_name} ({token_address[:10]}...)
Risk Score: {risk_score}/100

Red Flags:
{warning_text}

🔍 Do your own research before investing!

#CryptoWarning #DeFi #DYOR"""
        
        success = True
        
        # Post to Twitter
        if self.twitter_enabled:
            success = success and self._post_to_twitter(message)
        
        # Send to Overseer bot
        if self.overseer_enabled:
            alert_data = {
                'type': 'suspicious_token',
                'token_address': token_address,
                'token_name': token_name,
                'risk_score': risk_score,
                'warnings': warnings,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            success = success and self._send_to_overseer(alert_data)
        
        if success:
            logger.info(f"🔔 Posted suspicious token alert for {token_name}")
        
        return success
    
    def post_high_potential_alert(self, token_address: str, token_name: str,
                                  score: int, reasons: List[str]) -> bool:
        """
        Post an alert about a high-potential token (ape-worthy)
        
        Args:
            token_address: Token contract address
            token_name: Name of the token
            score: Potential score (0-100)
            reasons: List of positive indicators
            
        Returns:
            True if alert was posted successfully
        """
        if not self.enabled or not self.alert_on_high_potential:
            return False
        
        # Create alert message
        reasons_text = '\n'.join([f"✅ {r}" for r in reasons[:3]])
        
        message = f"""🚀 HIGH POTENTIAL TOKEN DETECTED

Token: {token_name} ({token_address[:10]}...)
Potential Score: {score}/100

Why it looks good:
{reasons_text}

⚠️ Not financial advice! DYOR!

#Crypto #DeFi #Gem #EarlyEntry"""
        
        success = True
        
        # Post to Twitter
        if self.twitter_enabled:
            success = success and self._post_to_twitter(message)
        
        # Send to Overseer bot
        if self.overseer_enabled:
            alert_data = {
                'type': 'high_potential',
                'token_address': token_address,
                'token_name': token_name,
                'score': score,
                'reasons': reasons,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            success = success and self._send_to_overseer(alert_data)
        
        if success:
            logger.info(f"🔔 Posted high potential alert for {token_name}")
        
        return success
    
    def _post_to_twitter(self, message: str) -> bool:
        """
        Post a message to Twitter
        
        Args:
            message: Message to post
            
        Returns:
            True if successful
        """
        if not self.twitter_enabled:
            return False
        
        try:
            # NOTE: This is a simplified implementation
            # In production, use tweepy or python-twitter library with OAuth 1.0a
            # For now, this is a placeholder that logs the attempt
            
            logger.info(f"📤 Would post to Twitter: {message[:50]}...")
            
            # TODO: Implement actual Twitter API integration
            # import tweepy
            # auth = tweepy.OAuthHandler(self.twitter_api_key, self.twitter_api_secret)
            # auth.set_access_token(self.twitter_access_token, self.twitter_access_secret)
            # api = tweepy.API(auth)
            # api.update_status(message)
            
            return True
            
        except Exception as e:
            logger.error(f"Error posting to Twitter: {e}")
            return False
    
    def _send_to_overseer(self, alert_data: Dict) -> bool:
        """
        Send alert to overseer-bot-ai via webhook
        
        Args:
            alert_data: Alert data dictionary
            
        Returns:
            True if successful
        """
        if not self.overseer_enabled or not self.overseer_webhook_url:
            return False
        
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            
            if self.overseer_api_key:
                headers['Authorization'] = f"Bearer {self.overseer_api_key}"
            
            response = requests.post(
                self.overseer_webhook_url,
                json=alert_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"✅ Sent alert to overseer bot: {alert_data['type']}")
                return True
            else:
                logger.warning(f"Overseer bot returned status {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending to overseer bot: {e}")
            return False
    
    def send_custom_alert(self, alert_type: str, data: Dict) -> bool:
        """
        Send a custom alert to overseer bot
        
        Args:
            alert_type: Type of alert
            data: Alert data
            
        Returns:
            True if successful
        """
        if not self.overseer_enabled:
            return False
        
        alert_data = {
            'type': alert_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        return self._send_to_overseer(alert_data)
