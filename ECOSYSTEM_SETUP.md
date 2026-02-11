# Ecosystem Setup Guide

## Overview

The Token Scalper ecosystem consists of three interconnected bots that work together to scan, detect, alert, and manage cryptocurrency tokens:

1. **Token-scalper** (this repository) - Core trading and scam detection engine
2. **overseer-bot-ai** - Twitter/X alert broadcaster
3. **overseer-bot-ui** - Dashboard and manual control center

This guide explains how to properly wire these bots together for unified event/webhook communication, heartbeat monitoring, and real-time ecosystem functionality.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     ECOSYSTEM ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐         Webhooks          ┌─────────────────────┐
│   Token-scalper      │────────────────────────────▶│ overseer-bot-ai     │
│  (Core Engine)       │                            │ (Twitter/X Bot)     │
│                      │                            │                     │
│ - Token scanning     │     Event Broadcasting     │ - Post alerts       │
│ - Auto trading       │◀───────────────────────────│ - Community alerts  │
│ - Rug detection      │                            │ - Social media      │
│ - Developer tracking │                            │                     │
└───────────┬──────────┘                            └──────────┬──────────┘
            │                                                  │
            │ Webhooks/API                                     │
            │                                                  │
            ▼                                                  ▼
┌──────────────────────┐        API Fetch          ┌─────────────────────┐
│  overseer-bot-ui     │────────────────────────────▶│  overseer-bot-ai    │
│  (Dashboard)         │                            │  (API Server)       │
│                      │                            │                     │
│ - Visual monitoring  │   Status & Control         │ - Status reports    │
│ - Manual controls    │◀───────────────────────────│ - Event history     │
│ - Analytics          │                            │ - Metrics API       │
│ - Configuration      │                            │                     │
└──────────────────────┘                            └─────────────────────┘
```

## Component Roles

### Token-scalper (This Bot)
- **Purpose**: Core trading and detection engine
- **Sends Events**: Rug pull alerts, suspicious tokens, high-potential tokens, trade executions, dev sell events
- **Receives Events**: Commands from overseer-bot-ui, status requests
- **Endpoints Provided**:
  - `POST /api/webhook/event` - Receive events from other bots
  - `POST /api/webhook/heartbeat` - Receive heartbeat from other bots
  - `GET /api/status/health` - Health check for monitoring
  - `GET /api/status/metrics` - Performance metrics

### overseer-bot-ai
- **Purpose**: Social media broadcaster and alert coordinator
- **Sends Events**: Community alerts, Twitter posts, status updates
- **Receives Events**: All alerts from Token-scalper
- **Expected Endpoints**:
  - `POST /api/webhook/event` - Receive events from Token-scalper
  - `GET /api/status` - Status information

### overseer-bot-ui
- **Purpose**: Human-friendly dashboard and control center
- **Sends Events**: Manual commands, configuration changes
- **Receives Events**: Status updates from both bots
- **Expected Endpoints**:
  - `POST /api/webhook/event` - Receive events from Token-scalper
  - `GET /api/dashboard` - Dashboard interface

## Quick Start

### Prerequisites

1. All three bots cloned and installed:
   ```bash
   # Token-scalper
   git clone https://github.com/Unwrenchable/Token-scalper
   cd Token-scalper
   pip install -r requirements.txt
   
   # overseer-bot-ai (example)
   git clone https://github.com/Unwrenchable/overseer-bot-ai
   cd overseer-bot-ai
   npm install
   
   # overseer-bot-ui (example)
   git clone https://github.com/Unwrenchable/overseer-bot-ui
   cd overseer-bot-ui
   npm install
   ```

2. Python 3.9+ for Token-scalper
3. Node.js 16+ for overseer bots (if applicable)

### Step-by-Step Setup

#### Step 1: Configure Token-scalper

1. Copy the example configuration:
   ```bash
   cd Token-scalper
   cp .env.example .env
   cp config.example.json config.json
   ```

2. Edit `.env` and add ecosystem configuration:
   ```bash
   # Ecosystem Integration
   ECOSYSTEM_BOT_ID="token-scalper-001"
   ECOSYSTEM_API_KEY="your_secure_api_key_here_change_me"
   ECOSYSTEM_SHARED_SECRET="your_shared_secret_here_change_me"
   
   # Webhook URLs (update with actual URLs after starting other bots)
   ECOSYSTEM_OVERSEER_AI_URL="http://localhost:3000/api/webhook/event"
   ECOSYSTEM_OVERSEER_UI_URL="http://localhost:4000/api/webhook/event"
   ```

3. Edit `config.json` to enable ecosystem integration:
   ```json
   {
     "ecosystem": {
       "enabled": true,
       "bot_id": "token-scalper-001",
       "bot_name": "Token Scalper",
       "broadcast_all_events": true,
       "retry_attempts": 3,
       "timeout_seconds": 10
     },
     "dashboard": {
       "enabled": true,
       "host": "0.0.0.0",
       "port": 5000
     }
   }
   ```

#### Step 2: Configure overseer-bot-ai

1. Add Token-scalper webhook endpoint to overseer-bot-ai configuration:
   ```bash
   # In overseer-bot-ai .env or config
   WEBHOOK_RECEIVER_PORT=3000
   TOKEN_SCALPER_WEBHOOK_URL="http://localhost:5000/api/webhook/event"
   API_KEY="your_secure_api_key_here_change_me"
   ```

2. Configure the webhook receiver endpoint in overseer-bot-ai to accept events from Token-scalper

#### Step 3: Configure overseer-bot-ui

1. Add API endpoints to overseer-bot-ui configuration:
   ```bash
   # In overseer-bot-ui .env or config
   UI_PORT=4000
   TOKEN_SCALPER_API="http://localhost:5000"
   OVERSEER_AI_API="http://localhost:3000"
   API_KEY="your_secure_api_key_here_change_me"
   ```

#### Step 4: Start All Bots

Start the bots in this order:

1. **Start Token-scalper**:
   ```bash
   cd Token-scalper
   python main.py
   # Dashboard available at http://localhost:5000
   ```

2. **Start overseer-bot-ai**:
   ```bash
   cd overseer-bot-ai
   npm start
   # API available at http://localhost:3000
   ```

3. **Start overseer-bot-ui**:
   ```bash
   cd overseer-bot-ui
   npm start
   # Dashboard available at http://localhost:4000
   ```

### Step 5: Verify Connectivity

Test the ecosystem connectivity:

1. **Check Token-scalper health**:
   ```bash
   curl http://localhost:5000/api/status/health
   ```

2. **Test webhook from Token-scalper to overseer-bot-ai**:
   ```bash
   # This would be done automatically by Token-scalper
   # You can verify in logs that events are being sent
   ```

3. **Check all bots are communicating**:
   - Token-scalper logs should show "✅ Event sent to overseer-ai"
   - overseer-bot-ai logs should show "📥 Received event from token-scalper"
   - overseer-bot-ui should display live data from both bots

## Event Schema

All ecosystem events follow a standardized schema:

```json
{
  "event_id": "token-scalper-001-abc123def456",
  "event_type": "rug_pull_alert|suspicious_token|high_potential|trade_executed|heartbeat|status_update",
  "source": {
    "bot_id": "token-scalper-001",
    "bot_name": "Token Scalper",
    "bot_type": "token-scalper"
  },
  "timestamp": "2024-01-01T12:00:00.000Z",
  "priority": "low|normal|high|critical",
  "data": {
    // Event-specific data
  },
  "schema_version": "1.0"
}
```

### Event Types

#### 1. Heartbeat
Sent periodically to indicate bot is alive and operational.

```json
{
  "event_type": "heartbeat",
  "priority": "low",
  "data": {
    "bot_id": "token-scalper-001",
    "status": "online",
    "uptime_seconds": 3600,
    "active_positions": 5,
    "total_trades": 42,
    "wallet_count": 3,
    "last_action": "buy_token",
    "health_metrics": {
      "rpc_healthy": true,
      "wallet_balance": "sufficient",
      "memory_usage_mb": 256
    }
  }
}
```

#### 2. Rug Pull Alert
Critical alert when rug pull detected.

```json
{
  "event_type": "rug_pull_alert",
  "priority": "critical",
  "data": {
    "token_address": "0x1234...",
    "token_name": "ScamToken",
    "alert_type": "rug_pull",
    "severity": "critical",
    "details": {
      "dev_address": "0xabcd...",
      "dev_sell_percent": 80,
      "liquidity_removed": true,
      "description": "Developer sold 80% and removed liquidity"
    }
  }
}
```

#### 3. Suspicious Token
Warning about potentially dangerous token.

```json
{
  "event_type": "suspicious_token",
  "priority": "high",
  "data": {
    "token_address": "0x5678...",
    "token_name": "SuspiciousToken",
    "alert_type": "suspicious",
    "severity": "high",
    "details": {
      "risk_score": 85,
      "warnings": [
        "High sell tax detected",
        "Low liquidity",
        "Unverified contract"
      ]
    }
  }
}
```

#### 4. High Potential Token
Alert about promising opportunity.

```json
{
  "event_type": "high_potential",
  "priority": "high",
  "data": {
    "token_address": "0x9abc...",
    "token_name": "MoonToken",
    "alert_type": "high_potential",
    "severity": "normal",
    "details": {
      "score": 92,
      "reasons": [
        "Strong liquidity",
        "Verified contract",
        "Good developer reputation"
      ]
    }
  }
}
```

#### 5. Trade Executed
Notification of completed trade.

```json
{
  "event_type": "trade_executed",
  "priority": "normal",
  "data": {
    "trade_type": "buy",
    "token_address": "0xdef0...",
    "token_name": "TestToken",
    "amount": 0.1,
    "price": 0.00000123,
    "wallet_address": "0x9876..."
  }
}
```

## Authentication

All webhook communications should be authenticated using one of two methods:

### Method 1: Bearer Token (Recommended)
```bash
Authorization: Bearer your_api_key_here
```

### Method 2: Shared Secret
```bash
X-Shared-Secret: your_shared_secret_here
```

**Important**: Use the same API key and shared secret across all bots for seamless communication.

## Testing Webhook Communication

### Manual Test: Send Event to Token-scalper

Test the Token-scalper webhook receiver:

```bash
curl -X POST http://localhost:5000/api/webhook/event \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key_here" \
  -d '{
    "event_id": "test-001",
    "event_type": "status_request",
    "source": {
      "bot_id": "manual-test",
      "bot_name": "Manual Test",
      "bot_type": "test"
    },
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'",
    "priority": "normal",
    "data": {}
  }'
```

Expected response:
```json
{
  "status": "success",
  "event_id": "test-001",
  "processed_at": "2024-01-01T12:00:00.000Z",
  "response": {
    "status": "online",
    "active_positions": 0,
    "total_trades": 0
  }
}
```

### Manual Test: Check Health Status

```bash
curl http://localhost:5000/api/status/health
```

Expected response:
```json
{
  "status": "healthy",
  "bot_id": "token-scalper-001",
  "bot_type": "token-scalper",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "uptime_seconds": 0,
  "components": {
    "dashboard": {
      "status": "healthy",
      "active_positions": 0,
      "recent_alerts": 0
    },
    "analytics": {
      "status": "healthy",
      "total_trades": 0,
      "total_profit_usd": 0
    },
    "webhooks": {
      "status": "configured",
      "auth_enabled": true
    }
  },
  "version": "2.0.0",
  "capabilities": [
    "token_scanning",
    "automated_trading",
    "rug_pull_detection",
    "developer_tracking",
    "webhook_events",
    "real_time_alerts"
  ]
}
```

## Integration Code Examples

### Token-scalper: Send Event

```python
from ecosystem_integration import EcosystemIntegration, EventType

# Initialize
config = {...}  # Your config
ecosystem = EcosystemIntegration(config)

# Send rug pull alert
ecosystem.broadcast_event(
    EventType.RUG_PULL_ALERT,
    {
        'token_address': '0x123...',
        'token_name': 'ScamToken',
        'alert_type': 'rug_pull',
        'severity': 'critical',
        'details': {...}
    },
    priority='critical'
)

# Send heartbeat
ecosystem.send_heartbeat({
    'status': 'online',
    'uptime_seconds': 3600,
    'active_positions': 5,
    'total_trades': 42
})
```

### overseer-bot-ai: Receive Event (Node.js Example)

```javascript
const express = require('express');
const app = express();

app.post('/api/webhook/event', express.json(), (req, res) => {
  const event = req.body;
  
  // Validate authentication
  const apiKey = req.headers['authorization']?.replace('Bearer ', '');
  if (apiKey !== process.env.API_KEY) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  // Process event
  console.log(`Received event: ${event.event_type} from ${event.source.bot_id}`);
  
  // Handle based on event type
  switch (event.event_type) {
    case 'rug_pull_alert':
      // Post to Twitter
      postToTwitter(event.data);
      break;
    case 'heartbeat':
      // Update status
      updateBotStatus(event.source.bot_id, event.data);
      break;
    // ... handle other event types
  }
  
  res.json({
    status: 'success',
    event_id: event.event_id,
    processed_at: new Date().toISOString()
  });
});

app.listen(3000, () => {
  console.log('overseer-bot-ai listening on port 3000');
});
```

## Troubleshooting

### Issue: Events Not Being Received

**Symptoms**: Token-scalper sends events but overseer-bot-ai doesn't receive them

**Solutions**:
1. Check webhook URLs are correct in `.env`
2. Verify both bots are running
3. Check API key matches on both sides
4. Check firewall/network settings
5. Look for errors in Token-scalper logs

### Issue: Authentication Errors

**Symptoms**: 401 Unauthorized responses

**Solutions**:
1. Ensure `ECOSYSTEM_API_KEY` matches in all bot configurations
2. Check that `Authorization` header is being sent
3. Verify the Bearer token format: `Bearer your_api_key`

### Issue: Events Timing Out

**Symptoms**: "Timeout sending to endpoint" errors

**Solutions**:
1. Check the receiving bot is responsive
2. Increase `timeout_seconds` in config
3. Check network latency
4. Verify the receiving bot's endpoint is correct

### Issue: Dashboard Not Showing Events

**Symptoms**: Dashboard loads but no live data

**Solutions**:
1. Enable dashboard in config: `"enabled": true`
2. Check dashboard is running on correct port
3. Refresh browser (auto-refresh is every 5 seconds)
4. Check browser console for errors
5. Verify API endpoints are accessible

## Production Deployment

### Security Best Practices

1. **Use HTTPS**: Always use HTTPS in production for webhook URLs
2. **Strong API Keys**: Generate cryptographically secure API keys
3. **Rotate Keys**: Regularly rotate API keys and secrets
4. **Network Security**: Use firewalls and VPNs to restrict access
5. **Monitor Logs**: Watch for unauthorized access attempts

### Deployment Checklist

- [ ] All bots installed and configured
- [ ] API keys generated and configured
- [ ] Webhook URLs use HTTPS
- [ ] Firewall rules configured
- [ ] Monitoring/alerting set up
- [ ] Backup strategy in place
- [ ] Documentation updated with actual URLs
- [ ] Test all webhook endpoints
- [ ] Verify event flow end-to-end
- [ ] Set up log aggregation
- [ ] Configure error notifications

### Recommended Architecture

For production, consider:
- **Load Balancer**: For high availability
- **Message Queue**: Redis/RabbitMQ for event buffering
- **Database**: PostgreSQL/MongoDB for persistent storage
- **Monitoring**: Prometheus + Grafana for metrics
- **Logging**: ELK stack or similar
- **Containerization**: Docker for consistent deployment
- **Orchestration**: Kubernetes for scaling

## Support

For issues or questions:
- Token-scalper: https://github.com/Unwrenchable/Token-scalper/issues
- overseer-bot-ai: https://github.com/Unwrenchable/overseer-bot-ai/issues
- overseer-bot-ui: https://github.com/Unwrenchable/overseer-bot-ui/issues

## License

See individual repository licenses.
