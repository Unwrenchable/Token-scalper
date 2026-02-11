# Token Scalper API Documentation

## Overview

Token Scalper provides REST API endpoints for ecosystem integration, monitoring, and webhook communication.

## Base URL

```
http://localhost:5000/api
```

## Authentication

All webhook endpoints require authentication using one of these methods:

### Bearer Token
```bash
Authorization: Bearer YOUR_API_KEY
```

### Shared Secret
```bash
X-Shared-Secret: YOUR_SHARED_SECRET
```

## Endpoints

### 1. Health Check

Check bot health and status.

**Endpoint:** `GET /api/status/health`

**Authentication:** None required

**Response:**
```json
{
  "status": "healthy",
  "bot_id": "token-scalper-001",
  "bot_type": "token-scalper",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "uptime_seconds": 3600,
  "components": {
    "dashboard": {
      "status": "healthy",
      "active_positions": 5,
      "recent_alerts": 10
    },
    "analytics": {
      "status": "healthy",
      "total_trades": 42,
      "total_profit_usd": 1234.56
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

### 2. Metrics

Get performance metrics for monitoring systems.

**Endpoint:** `GET /api/status/metrics`

**Authentication:** None required

**Response:**
```json
{
  "token_scalper_total_trades": 42,
  "token_scalper_successful_trades": 38,
  "token_scalper_rug_pulls_avoided": 4,
  "token_scalper_total_profit_usd": 1234.56,
  "token_scalper_active_positions": 5,
  "token_scalper_tracked_developers": 23,
  "token_scalper_flagged_developers": 3,
  "token_scalper_recent_alerts": 10,
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### 3. Receive Webhook Event

Receive events from other ecosystem bots.

**Endpoint:** `POST /api/webhook/event`

**Authentication:** Required (Bearer token or Shared Secret)

**Request Body:**
```json
{
  "event_id": "overseer-ai-001-abc123",
  "event_type": "command|status_request|alert",
  "source": {
    "bot_id": "overseer-ai-001",
    "bot_name": "Overseer Bot AI",
    "bot_type": "overseer-bot-ai"
  },
  "timestamp": "2024-01-01T12:00:00.000Z",
  "priority": "low|normal|high|critical",
  "data": {
    // Event-specific data
  }
}
```

**Response:**
```json
{
  "status": "success",
  "event_id": "overseer-ai-001-abc123",
  "processed_at": "2024-01-01T12:00:05.000Z",
  "response": {
    // Event-specific response data
  }
}
```

**Event Types:**

#### status_request
Request current bot status.

```json
{
  "event_type": "status_request",
  "data": {}
}
```

Response:
```json
{
  "response": {
    "status": "online",
    "active_positions": 5,
    "total_trades": 42
  }
}
```

#### command
Send a command to the bot.

```json
{
  "event_type": "command",
  "data": {
    "command": "pause_trading",
    "parameters": {}
  }
}
```

Response:
```json
{
  "response": {
    "command": "pause_trading",
    "result": "acknowledged",
    "note": "Command processing not yet implemented"
  }
}
```

#### alert
Send an alert to be displayed on the dashboard.

```json
{
  "event_type": "alert",
  "data": {
    "message": "External system alert",
    "severity": "warning"
  }
}
```

Response:
```json
{
  "response": {
    "result": "alert_stored"
  }
}
```

### 4. Receive Heartbeat

Receive heartbeat/status updates from other bots.

**Endpoint:** `POST /api/webhook/heartbeat`

**Authentication:** Required (Bearer token or Shared Secret)

**Request Body:**
```json
{
  "bot_id": "overseer-ai-001",
  "bot_name": "Overseer Bot AI",
  "status": "online",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "uptime_seconds": 7200,
  "metadata": {
    // Optional metadata
  }
}
```

**Response:**
```json
{
  "status": "acknowledged",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### 5. Get Status

Get current bot status.

**Endpoint:** `GET /api/status`

**Authentication:** None required

**Response:**
```json
{
  "status": "online",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "active_positions": 5,
  "tracked_wallets": 3,
  "recent_alerts": 10
}
```

### 6. Get Active Positions

Get list of active trading positions.

**Endpoint:** `GET /api/positions`

**Authentication:** None required

**Response:**
```json
[
  {
    "token_name": "TestToken",
    "token_address": "0x123...",
    "profit": 15.5,
    "profit_percent": 15.5,
    "entry_time": "2024-01-01T10:00:00.000Z"
  }
]
```

### 7. Get Alerts

Get recent alerts.

**Endpoint:** `GET /api/alerts?limit=20`

**Authentication:** None required

**Query Parameters:**
- `limit` (optional): Number of alerts to return (default: 20)

**Response:**
```json
[
  {
    "type": "rug_pull",
    "message": "Rug pull detected on ScamToken",
    "severity": "danger",
    "timestamp": "2024-01-01T11:30:00.000Z"
  },
  {
    "type": "high_potential",
    "message": "High potential token detected: MoonToken",
    "severity": "success",
    "timestamp": "2024-01-01T11:15:00.000Z"
  }
]
```

### 8. Get Analytics

Get trading analytics.

**Endpoint:** `GET /api/analytics`

**Authentication:** None required

**Response:**
```json
{
  "total_trades": 42,
  "successful_trades": 38,
  "rug_pulls_avoided": 4,
  "total_profit_usd": 1234.56
}
```

### 9. Get Developer Statistics

Get developer tracking statistics.

**Endpoint:** `GET /api/developer-stats`

**Authentication:** None required

**Response:**
```json
{
  "total_developers": 23,
  "scam_developers": 3,
  "total_projects": 45,
  "rugged_projects": 5
}
```

## Outgoing Webhook Events

Token Scalper sends events to configured webhook URLs when significant events occur.

### Event Schema

All outgoing events follow this schema:

```json
{
  "event_id": "token-scalper-001-unique-id",
  "event_type": "event_name",
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

#### heartbeat
Periodic status update (sent every 60 seconds by default).

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

#### rug_pull_alert
Critical alert when rug pull is detected.

```json
{
  "event_type": "rug_pull_alert",
  "priority": "critical",
  "data": {
    "token_address": "0x1234567890abcdef1234567890abcdef12345678",
    "token_name": "ScamToken",
    "alert_type": "rug_pull",
    "severity": "critical",
    "details": {
      "dev_address": "0xabcdef1234567890abcdef1234567890abcdef12",
      "dev_sell_percent": 80,
      "liquidity_removed": true,
      "description": "Developer sold 80% of holdings and removed liquidity"
    }
  }
}
```

#### suspicious_token
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

#### high_potential
Alert about promising token opportunity.

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

#### trade_executed
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

## Error Responses

All endpoints return standardized error responses:

**400 Bad Request**
```json
{
  "error": "Invalid request: Missing required field 'event_id'"
}
```

**401 Unauthorized**
```json
{
  "error": "Unauthorized: Invalid or missing authentication"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal server error: <error message>"
}
```

## Rate Limiting

Currently no rate limiting is implemented. For production use, consider implementing rate limiting on webhook endpoints.

## Examples

### cURL: Send Status Request

```bash
curl -X POST http://localhost:5000/api/webhook/event \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "event_id": "test-001",
    "event_type": "status_request",
    "source": {
      "bot_id": "test-bot",
      "bot_name": "Test Bot",
      "bot_type": "test"
    },
    "timestamp": "2024-01-01T12:00:00.000Z",
    "priority": "normal",
    "data": {}
  }'
```

### Python: Send Event

```python
import requests

url = "http://localhost:5000/api/webhook/event"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
}
payload = {
    "event_id": "test-001",
    "event_type": "alert",
    "source": {
        "bot_id": "python-client",
        "bot_name": "Python Client",
        "bot_type": "client"
    },
    "timestamp": "2024-01-01T12:00:00.000Z",
    "priority": "normal",
    "data": {
        "message": "Test alert from Python",
        "severity": "info"
    }
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### JavaScript/Node.js: Receive Event

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
  
  console.log(`Received event: ${event.event_type}`);
  
  // Process event
  // ...
  
  res.json({
    status: 'success',
    event_id: event.event_id,
    processed_at: new Date().toISOString()
  });
});

app.listen(3000);
```

## Support

For issues or questions, please visit:
https://github.com/Unwrenchable/Token-scalper/issues
