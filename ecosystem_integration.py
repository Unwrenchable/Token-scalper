"""
Ecosystem Integration Module
Handles unified event/webhook communication between Token-scalper, overseer-bot-ai, and overseer-bot-ui
"""

import logging
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Standard event types for ecosystem communication"""
    TOKEN_DETECTED = "token_detected"
    RUG_PULL_ALERT = "rug_pull_alert"
    SUSPICIOUS_TOKEN = "suspicious_token"
    HIGH_POTENTIAL = "high_potential"
    TRADE_EXECUTED = "trade_executed"
    POSITION_UPDATE = "position_update"
    DEV_SELL_EVENT = "dev_sell_event"
    HEARTBEAT = "heartbeat"
    STATUS_UPDATE = "status_update"
    SYSTEM_ALERT = "system_alert"


class EcosystemIntegration:
    """
    Unified ecosystem integration handler
    Manages event broadcasting to overseer-bot-ai and overseer-bot-ui
    """
    
    def __init__(self, config: Dict):
        """
        Initialize ecosystem integration
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.eco_config = config.get('ecosystem', {})
        
        # Bot identification
        self.bot_id = self.eco_config.get('bot_id', 'token-scalper-001')
        self.bot_name = self.eco_config.get('bot_name', 'Token Scalper')
        
        # Webhook endpoints
        self.overseer_ai_url = self.eco_config.get('overseer_ai_webhook_url', '')
        self.overseer_ui_url = self.eco_config.get('overseer_ui_webhook_url', '')
        self.custom_webhooks = self.eco_config.get('custom_webhook_urls', [])
        
        # Authentication
        self.api_key = self.eco_config.get('api_key', '')
        self.shared_secret = self.eco_config.get('shared_secret', '')
        
        # Settings
        self.enabled = self.eco_config.get('enabled', False)
        self.broadcast_all = self.eco_config.get('broadcast_all_events', True)
        self.retry_attempts = self.eco_config.get('retry_attempts', 3)
        self.timeout_seconds = self.eco_config.get('timeout_seconds', 10)
        
        # Event filtering
        self.event_filters = self.eco_config.get('event_filters', {})
        
        if self.enabled:
            logger.info("🌐 Ecosystem Integration initialized")
            logger.info(f"   Bot ID: {self.bot_id}")
            logger.info(f"   Overseer AI: {'✅' if self.overseer_ai_url else '❌'}")
            logger.info(f"   Overseer UI: {'✅' if self.overseer_ui_url else '❌'}")
            logger.info(f"   Custom Webhooks: {len(self.custom_webhooks)}")
    
    def broadcast_event(self, event_type: EventType, data: Dict, 
                       priority: str = "normal") -> Dict[str, bool]:
        """
        Broadcast an event to all registered endpoints
        
        Args:
            event_type: Type of event
            data: Event data payload
            priority: Priority level (low, normal, high, critical)
            
        Returns:
            Dictionary with delivery status for each endpoint
        """
        if not self.enabled:
            logger.debug("Ecosystem integration disabled, skipping broadcast")
            return {}
        
        # Check event filters
        if not self._should_broadcast_event(event_type):
            logger.debug(f"Event {event_type.value} filtered, skipping broadcast")
            return {}
        
        # Build event payload
        event = self._build_event_payload(event_type, data, priority)
        
        results = {}
        
        # Send to overseer-bot-ai
        if self.overseer_ai_url:
            results['overseer-ai'] = self._send_to_endpoint(
                self.overseer_ai_url, event, 'overseer-ai'
            )
        
        # Send to overseer-bot-ui
        if self.overseer_ui_url:
            results['overseer-ui'] = self._send_to_endpoint(
                self.overseer_ui_url, event, 'overseer-ui'
            )
        
        # Send to custom webhooks
        for idx, webhook_url in enumerate(self.custom_webhooks):
            webhook_name = f"custom-webhook-{idx+1}"
            results[webhook_name] = self._send_to_endpoint(
                webhook_url, event, webhook_name
            )
        
        return results
    
    def send_heartbeat(self, status_data: Dict) -> Dict[str, bool]:
        """
        Send heartbeat/status update to ecosystem
        
        Args:
            status_data: Bot status information
            
        Returns:
            Delivery status for each endpoint
        """
        heartbeat_data = {
            'bot_id': self.bot_id,
            'bot_name': self.bot_name,
            'status': status_data.get('status', 'online'),
            'uptime_seconds': status_data.get('uptime_seconds', 0),
            'active_positions': status_data.get('active_positions', 0),
            'total_trades': status_data.get('total_trades', 0),
            'wallet_count': status_data.get('wallet_count', 0),
            'last_action': status_data.get('last_action', 'idle'),
            'health_metrics': status_data.get('health_metrics', {})
        }
        
        return self.broadcast_event(EventType.HEARTBEAT, heartbeat_data, priority='low')
    
    def send_token_alert(self, token_address: str, token_name: str,
                        alert_type: str, severity: str, details: Dict) -> Dict[str, bool]:
        """
        Send token-related alert to ecosystem
        
        Args:
            token_address: Token contract address
            token_name: Token name
            alert_type: Type of alert (rug_pull, suspicious, high_potential)
            severity: Severity level
            details: Additional alert details
            
        Returns:
            Delivery status for each endpoint
        """
        alert_data = {
            'token_address': token_address,
            'token_name': token_name,
            'alert_type': alert_type,
            'severity': severity,
            'details': details
        }
        
        # Map alert type to event type
        event_type_map = {
            'rug_pull': EventType.RUG_PULL_ALERT,
            'suspicious': EventType.SUSPICIOUS_TOKEN,
            'high_potential': EventType.HIGH_POTENTIAL
        }
        
        event_type = event_type_map.get(alert_type, EventType.SYSTEM_ALERT)
        priority = 'critical' if alert_type == 'rug_pull' else 'high'
        
        return self.broadcast_event(event_type, alert_data, priority=priority)
    
    def send_trade_notification(self, trade_type: str, token_address: str,
                               token_name: str, amount: float, price: float,
                               wallet_address: str) -> Dict[str, bool]:
        """
        Send trade execution notification
        
        Args:
            trade_type: Type of trade (buy, sell)
            token_address: Token contract address
            token_name: Token name
            amount: Trade amount
            price: Execution price
            wallet_address: Wallet used for trade
            
        Returns:
            Delivery status for each endpoint
        """
        trade_data = {
            'trade_type': trade_type,
            'token_address': token_address,
            'token_name': token_name,
            'amount': amount,
            'price': price,
            'wallet_address': wallet_address
        }
        
        return self.broadcast_event(EventType.TRADE_EXECUTED, trade_data, priority='normal')
    
    def _build_event_payload(self, event_type: EventType, data: Dict,
                           priority: str) -> Dict:
        """
        Build standardized event payload
        
        Args:
            event_type: Type of event
            data: Event data
            priority: Priority level
            
        Returns:
            Standardized event payload
        """
        return {
            'event_id': self._generate_event_id(),
            'event_type': event_type.value,
            'source': {
                'bot_id': self.bot_id,
                'bot_name': self.bot_name,
                'bot_type': 'token-scalper'
            },
            'timestamp': datetime.now().isoformat(),
            'priority': priority,
            'data': data,
            'schema_version': '1.0'
        }
    
    def _send_to_endpoint(self, url: str, event: Dict, endpoint_name: str) -> bool:
        """
        Send event to a specific endpoint with retry logic
        
        Args:
            url: Webhook URL
            event: Event payload
            endpoint_name: Name of endpoint for logging
            
        Returns:
            True if successful, False otherwise
        """
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': f'TokenScalper/{self.bot_id}',
            'X-Event-Type': event['event_type'],
            'X-Priority': event['priority']
        }
        
        # Add authentication headers
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        
        if self.shared_secret:
            headers['X-Shared-Secret'] = self.shared_secret
        
        # Retry logic
        for attempt in range(self.retry_attempts):
            try:
                response = requests.post(
                    url,
                    json=event,
                    headers=headers,
                    timeout=self.timeout_seconds
                )
                
                if response.status_code in [200, 201, 202, 204]:
                    logger.info(f"✅ Event sent to {endpoint_name}: {event['event_type']}")
                    return True
                else:
                    logger.warning(f"⚠️ {endpoint_name} returned status {response.status_code}")
                    
                    # Retry on server errors
                    if response.status_code >= 500 and attempt < self.retry_attempts - 1:
                        continue
                    
                    return False
                    
            except requests.exceptions.Timeout:
                logger.warning(f"⏱️ Timeout sending to {endpoint_name} (attempt {attempt+1})")
                if attempt < self.retry_attempts - 1:
                    continue
                return False
                
            except Exception as e:
                logger.error(f"❌ Error sending to {endpoint_name}: {e}")
                if attempt < self.retry_attempts - 1:
                    continue
                return False
        
        return False
    
    def _should_broadcast_event(self, event_type: EventType) -> bool:
        """
        Check if event should be broadcast based on filters
        
        Args:
            event_type: Type of event
            
        Returns:
            True if event should be broadcast
        """
        if self.broadcast_all:
            return True
        
        # Check event-specific filters
        event_name = event_type.value
        return self.event_filters.get(event_name, True)
    
    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        import uuid
        return f"{self.bot_id}-{uuid.uuid4().hex[:12]}"
    
    def get_status(self) -> Dict:
        """
        Get ecosystem integration status
        
        Returns:
            Status dictionary
        """
        return {
            'enabled': self.enabled,
            'bot_id': self.bot_id,
            'bot_name': self.bot_name,
            'overseer_ai_configured': bool(self.overseer_ai_url),
            'overseer_ui_configured': bool(self.overseer_ui_url),
            'custom_webhooks_count': len(self.custom_webhooks),
            'broadcast_all_events': self.broadcast_all
        }


def create_sample_event_schemas():
    """
    Create sample event schemas for documentation
    
    Returns:
        Dictionary of sample event payloads
    """
    return {
        'heartbeat': {
            'event_id': 'token-scalper-001-abc123def456',
            'event_type': 'heartbeat',
            'source': {
                'bot_id': 'token-scalper-001',
                'bot_name': 'Token Scalper',
                'bot_type': 'token-scalper'
            },
            'timestamp': '2024-01-01T12:00:00.000Z',
            'priority': 'low',
            'data': {
                'bot_id': 'token-scalper-001',
                'bot_name': 'Token Scalper',
                'status': 'online',
                'uptime_seconds': 3600,
                'active_positions': 5,
                'total_trades': 42,
                'wallet_count': 3,
                'last_action': 'buy_token',
                'health_metrics': {
                    'rpc_healthy': True,
                    'wallet_balance': 'sufficient',
                    'memory_usage_mb': 256
                }
            },
            'schema_version': '1.0'
        },
        'rug_pull_alert': {
            'event_id': 'token-scalper-001-xyz789ghi012',
            'event_type': 'rug_pull_alert',
            'source': {
                'bot_id': 'token-scalper-001',
                'bot_name': 'Token Scalper',
                'bot_type': 'token-scalper'
            },
            'timestamp': '2024-01-01T12:05:00.000Z',
            'priority': 'critical',
            'data': {
                'token_address': '0x1234567890abcdef1234567890abcdef12345678',
                'token_name': 'ScamToken',
                'alert_type': 'rug_pull',
                'severity': 'critical',
                'details': {
                    'dev_address': '0xabcdef1234567890abcdef1234567890abcdef12',
                    'dev_sell_percent': 80,
                    'liquidity_removed': True,
                    'description': 'Developer sold 80% of holdings and removed liquidity'
                }
            },
            'schema_version': '1.0'
        },
        'trade_executed': {
            'event_id': 'token-scalper-001-mno345pqr678',
            'event_type': 'trade_executed',
            'source': {
                'bot_id': 'token-scalper-001',
                'bot_name': 'Token Scalper',
                'bot_type': 'token-scalper'
            },
            'timestamp': '2024-01-01T12:10:00.000Z',
            'priority': 'normal',
            'data': {
                'trade_type': 'buy',
                'token_address': '0xfedcba0987654321fedcba0987654321fedcba09',
                'token_name': 'MoonToken',
                'amount': 0.1,
                'price': 0.00000123,
                'wallet_address': '0x9876543210fedcba9876543210fedcba98765432'
            },
            'schema_version': '1.0'
        }
    }
