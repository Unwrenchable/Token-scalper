# Ecosystem Integration Quick Reference

## Quick Start

### 1. Enable Ecosystem Integration

Edit your `.env` file:
```bash
# Ecosystem Integration
ECOSYSTEM_BOT_ID="token-scalper-001"
ECOSYSTEM_API_KEY="your_secure_random_api_key_here"
ECOSYSTEM_SHARED_SECRET="your_secure_random_secret_here"
ECOSYSTEM_OVERSEER_AI_URL="http://localhost:3000/api/webhook/event"
ECOSYSTEM_OVERSEER_UI_URL="http://localhost:4000/api/webhook/event"
```

### 2. Generate Secure Keys

```bash
# Generate API key (Linux/Mac)
openssl rand -hex 32

# Generate API key (Python)
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Test Connection

```bash
# Start Token-scalper with dashboard
python main.py

# In another terminal, test health endpoint
curl http://localhost:5000/api/status/health

# Test webhook endpoint (requires auth)
curl -X POST http://localhost:5000/api/webhook/event \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"event_id":"test","event_type":"status_request","source":{"bot_id":"test"},"timestamp":"2024-01-01T12:00:00Z","priority":"normal","data":{}}'
```

## Using Ecosystem Integration in Code

### Initialize

```python
from ecosystem_integration import EcosystemIntegration, EventType

config = {
    'ecosystem': {
        'enabled': True,
        'bot_id': 'token-scalper-001',
        'overseer_ai_webhook_url': 'http://localhost:3000/webhook',
        'api_key': 'your_api_key'
    }
}

ecosystem = EcosystemIntegration(config)
```

### Send Events

```python
# Send rug pull alert
ecosystem.send_token_alert(
    token_address='0x123...',
    token_name='ScamToken',
    alert_type='rug_pull',
    severity='critical',
    details={
        'dev_address': '0xabc...',
        'description': 'Developer sold 80% of holdings'
    }
)

# Send trade notification
ecosystem.send_trade_notification(
    trade_type='buy',
    token_address='0x456...',
    token_name='MoonToken',
    amount=0.1,
    price=0.00001,
    wallet_address='0xdef...'
)

# Send heartbeat
ecosystem.send_heartbeat({
    'status': 'online',
    'uptime_seconds': 3600,
    'active_positions': 5,
    'total_trades': 42
})
```

### Broadcast Custom Events

```python
# Broadcast any event type
ecosystem.broadcast_event(
    EventType.SYSTEM_ALERT,
    {
        'message': 'Custom system alert',
        'level': 'warning'
    },
    priority='high'
)
```

## API Endpoints

### Health Check
```bash
GET /api/status/health
# No auth required
```

### Metrics
```bash
GET /api/status/metrics
# No auth required
```

### Receive Webhook Event
```bash
POST /api/webhook/event
# Requires: Authorization: Bearer YOUR_API_KEY
# Or: X-Shared-Secret: YOUR_SECRET
```

### Receive Heartbeat
```bash
POST /api/webhook/heartbeat
# Requires: Authorization: Bearer YOUR_API_KEY
```

## Event Types

- `heartbeat` - Periodic status update
- `rug_pull_alert` - Critical rug pull detected
- `suspicious_token` - Warning about risky token
- `high_potential` - High-quality opportunity found
- `trade_executed` - Trade completed
- `position_update` - Position status changed
- `dev_sell_event` - Developer selling detected
- `status_update` - Bot status changed
- `system_alert` - System-level alert

## Authentication

Two methods supported:

1. **Bearer Token** (Recommended)
   ```bash
   Authorization: Bearer YOUR_API_KEY
   ```

2. **Shared Secret**
   ```bash
   X-Shared-Secret: YOUR_SECRET
   ```

## Configuration Options

```json
{
  "ecosystem": {
    "enabled": true,
    "bot_id": "token-scalper-001",
    "bot_name": "Token Scalper",
    "overseer_ai_webhook_url": "",
    "overseer_ui_webhook_url": "",
    "custom_webhook_urls": [],
    "api_key": "",
    "shared_secret": "",
    "broadcast_all_events": true,
    "retry_attempts": 3,
    "timeout_seconds": 10,
    "event_filters": {
      "heartbeat": true,
      "rug_pull_alert": true,
      "suspicious_token": true,
      "high_potential": true,
      "trade_executed": true
    }
  }
}
```

## Troubleshooting

### Events not being sent
- Check `enabled: true` in config
- Verify webhook URLs are correct
- Check logs for connection errors
- Verify target bot is running

### Authentication errors
- Ensure API key matches on both sides
- Check for typos in Authorization header
- Verify Bearer token format

### Connection timeouts
- Check network connectivity
- Verify target bot endpoint is accessible
- Increase `timeout_seconds` in config

## Resources

- [ECOSYSTEM_SETUP.md](ECOSYSTEM_SETUP.md) - Full deployment guide
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Complete API reference
- [test_ecosystem_integration.py](test_ecosystem_integration.py) - Testing script

## Support

Issues: https://github.com/Unwrenchable/Token-scalper/issues
