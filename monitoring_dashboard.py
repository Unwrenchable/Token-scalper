"""
Web-based Monitoring Dashboard
Real-time monitoring interface for wallet tracking and analytics
"""

from flask import Flask, render_template, jsonify, request, abort
import logging
import os
from typing import Dict, List
from datetime import datetime, timedelta
import json
import hmac
import hashlib
from functools import wraps

logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
# Load secret key from environment or generate a secure random one
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', os.urandom(24).hex())
# Webhook authentication
WEBHOOK_API_KEY = os.getenv('ECOSYSTEM_API_KEY', '')
WEBHOOK_SHARED_SECRET = os.getenv('ECOSYSTEM_SHARED_SECRET', '')

# Global state (in production, use Redis or database)
dashboard_state = {
    'active_positions': [],
    'tracked_wallets': [],
    'recent_alerts': [],
    'developer_stats': {},
    'analytics': {
        'total_trades': 0,
        'successful_trades': 0,
        'rug_pulls_avoided': 0,
        'total_profit_usd': 0
    }
}


class MonitoringDashboard:
    """
    Web-based monitoring dashboard for the token scalper bot
    """
    
    def __init__(self, config: Dict, dev_tracker=None, social_alerts=None):
        """
        Initialize monitoring dashboard
        
        Args:
            config: Configuration dictionary
            dev_tracker: DevReputationTracker instance
            social_alerts: SocialMediaAlerts instance
        """
        self.config = config
        self.dashboard_config = config.get('dashboard', {})
        self.enabled = self.dashboard_config.get('enabled', False)
        
        # Support PORT environment variable for deployment platforms (Render, Heroku, etc.)
        self.port = int(os.getenv('PORT', self.dashboard_config.get('port', 5000)))
        self.host = self.dashboard_config.get('host', '127.0.0.1')
        
        self.dev_tracker = dev_tracker
        self.social_alerts = social_alerts
        
        if self.enabled:
            logger.info(f"📊 Dashboard will be available at http://{self.host}:{self.port}")
    
    def update_positions(self, positions: List[Dict]):
        """Update active positions"""
        dashboard_state['active_positions'] = positions
    
    def update_tracked_wallets(self, wallets: List[Dict]):
        """Update tracked wallets"""
        dashboard_state['tracked_wallets'] = wallets
    
    def add_alert(self, alert_type: str, message: str, severity: str = 'info'):
        """Add a new alert"""
        alert = {
            'type': alert_type,
            'message': message,
            'severity': severity,
            'timestamp': datetime.now().isoformat()
        }
        dashboard_state['recent_alerts'].insert(0, alert)
        # Keep only last 50 alerts
        dashboard_state['recent_alerts'] = dashboard_state['recent_alerts'][:50]
    
    def update_analytics(self, analytics: Dict):
        """Update analytics data"""
        dashboard_state['analytics'].update(analytics)
    
    def update_developer_stats(self, stats: Dict):
        """Update developer statistics"""
        dashboard_state['developer_stats'] = stats
    
    def run(self):
        """Start the dashboard web server"""
        if not self.enabled:
            logger.info("Dashboard is disabled in config")
            return
        
        logger.info(f"🚀 Starting dashboard on {self.host}:{self.port}")
        app.run(host=self.host, port=self.port, debug=False)


# Flask routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/status')
def api_status():
    """Get current status"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'active_positions': len(dashboard_state['active_positions']),
        'tracked_wallets': len(dashboard_state['tracked_wallets']),
        'recent_alerts': len(dashboard_state['recent_alerts'])
    })


@app.route('/api/positions')
def api_positions():
    """Get active positions"""
    return jsonify(dashboard_state['active_positions'])


@app.route('/api/wallets')
def api_wallets():
    """Get tracked wallets"""
    return jsonify(dashboard_state['tracked_wallets'])


@app.route('/api/alerts')
def api_alerts():
    """Get recent alerts"""
    limit = request.args.get('limit', 20, type=int)
    return jsonify(dashboard_state['recent_alerts'][:limit])


@app.route('/api/analytics')
def api_analytics():
    """Get analytics data"""
    return jsonify(dashboard_state['analytics'])


@app.route('/api/developer-stats')
def api_developer_stats():
    """Get developer statistics"""
    return jsonify(dashboard_state['developer_stats'])


@app.route('/api/search-developer/<address>')
def api_search_developer(address):
    """Search for developer by address"""
    # This would query the dev_tracker
    return jsonify({
        'address': address,
        'found': False,
        'message': 'Developer tracking integration pending'
    })


# =============================================================================
# WEBHOOK AUTHENTICATION & ECOSYSTEM INTEGRATION ENDPOINTS
# =============================================================================

def require_webhook_auth(f):
    """Decorator to require webhook authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if authentication is configured
        if not WEBHOOK_API_KEY and not WEBHOOK_SHARED_SECRET:
            # No auth configured, allow all (development mode)
            logger.warning("Webhook auth not configured - accepting all requests")
            return f(*args, **kwargs)
        
        # Check Bearer token
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer ') and WEBHOOK_API_KEY:
            token = auth_header[7:]
            if token == WEBHOOK_API_KEY:
                return f(*args, **kwargs)
        
        # Check shared secret
        secret_header = request.headers.get('X-Shared-Secret', '')
        if secret_header and WEBHOOK_SHARED_SECRET:
            if secret_header == WEBHOOK_SHARED_SECRET:
                return f(*args, **kwargs)
        
        # Authentication failed
        logger.warning(f"Unauthorized webhook access attempt from {request.remote_addr}")
        abort(401, description="Unauthorized: Invalid or missing authentication")
    
    return decorated_function


@app.route('/api/webhook/event', methods=['POST'])
@require_webhook_auth
def webhook_receive_event():
    """
    Receive events from other ecosystem bots (overseer-bot-ai, overseer-bot-ui)
    
    Expected payload:
    {
        "event_id": "unique-event-id",
        "event_type": "command|status_request|alert",
        "source": {
            "bot_id": "overseer-ai-001",
            "bot_name": "Overseer Bot AI",
            "bot_type": "overseer-bot-ai"
        },
        "timestamp": "2024-01-01T12:00:00.000Z",
        "priority": "low|normal|high|critical",
        "data": { ... }
    }
    """
    try:
        event = request.get_json()
        
        if not event:
            return jsonify({'error': 'No JSON payload provided'}), 400
        
        # Validate required fields
        required_fields = ['event_id', 'event_type', 'source', 'timestamp']
        for field in required_fields:
            if field not in event:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        event_type = event['event_type']
        source = event['source']
        data = event.get('data', {})
        
        logger.info(f"📥 Received webhook event: {event_type} from {source.get('bot_id', 'unknown')}")
        
        # Process event based on type
        response_data = _process_webhook_event(event_type, source, data)
        
        # Add to recent alerts for dashboard visibility
        dashboard_state['recent_alerts'].insert(0, {
            'type': f"webhook_{event_type}",
            'message': f"Event from {source.get('bot_name', 'unknown')}: {event_type}",
            'severity': 'info',
            'timestamp': datetime.now().isoformat()
        })
        dashboard_state['recent_alerts'] = dashboard_state['recent_alerts'][:50]
        
        return jsonify({
            'status': 'success',
            'event_id': event['event_id'],
            'processed_at': datetime.now().isoformat(),
            'response': response_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook event: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/webhook/heartbeat', methods=['POST'])
@require_webhook_auth
def webhook_receive_heartbeat():
    """
    Receive heartbeat from other ecosystem bots
    Allows overseer-bot-ai and overseer-bot-ui to report their status
    """
    try:
        heartbeat = request.get_json()
        
        if not heartbeat:
            return jsonify({'error': 'No JSON payload provided'}), 400
        
        bot_id = heartbeat.get('bot_id', 'unknown')
        status = heartbeat.get('status', 'unknown')
        
        logger.debug(f"💓 Heartbeat from {bot_id}: {status}")
        
        # Store heartbeat info (in production, use Redis or database)
        # For now, just acknowledge
        
        return jsonify({
            'status': 'acknowledged',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing heartbeat: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/status/health', methods=['GET'])
def api_health_check():
    """
    Health check endpoint for ecosystem monitoring
    Returns detailed system health information
    """
    try:
        health_status = {
            'status': 'healthy',
            'bot_id': os.getenv('ECOSYSTEM_BOT_ID', 'token-scalper-001'),
            'bot_type': 'token-scalper',
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': _calculate_uptime(),
            'components': {
                'dashboard': {
                    'status': 'healthy',
                    'active_positions': len(dashboard_state['active_positions']),
                    'recent_alerts': len(dashboard_state['recent_alerts'])
                },
                'analytics': {
                    'status': 'healthy',
                    'total_trades': dashboard_state['analytics'].get('total_trades', 0),
                    'total_profit_usd': dashboard_state['analytics'].get('total_profit_usd', 0)
                },
                'webhooks': {
                    'status': 'configured' if WEBHOOK_API_KEY or WEBHOOK_SHARED_SECRET else 'unconfigured',
                    'auth_enabled': bool(WEBHOOK_API_KEY or WEBHOOK_SHARED_SECRET)
                }
            },
            'version': '2.0.0',
            'capabilities': [
                'token_scanning',
                'automated_trading',
                'rug_pull_detection',
                'developer_tracking',
                'webhook_events',
                'real_time_alerts'
            ]
        }
        
        return jsonify(health_status), 200
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/status/metrics', methods=['GET'])
def api_metrics():
    """
    Metrics endpoint for Prometheus or other monitoring systems
    Returns key performance metrics
    """
    try:
        metrics = {
            'token_scalper_total_trades': dashboard_state['analytics'].get('total_trades', 0),
            'token_scalper_successful_trades': dashboard_state['analytics'].get('successful_trades', 0),
            'token_scalper_rug_pulls_avoided': dashboard_state['analytics'].get('rug_pulls_avoided', 0),
            'token_scalper_total_profit_usd': dashboard_state['analytics'].get('total_profit_usd', 0),
            'token_scalper_active_positions': len(dashboard_state['active_positions']),
            'token_scalper_tracked_developers': dashboard_state['developer_stats'].get('total_developers', 0),
            'token_scalper_flagged_developers': dashboard_state['developer_stats'].get('scam_developers', 0),
            'token_scalper_recent_alerts': len(dashboard_state['recent_alerts']),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(metrics), 200
        
    except Exception as e:
        logger.error(f"Error fetching metrics: {e}")
        return jsonify({'error': str(e)}), 500


def _process_webhook_event(event_type: str, source: Dict, data: Dict) -> Dict:
    """
    Process incoming webhook event
    
    Args:
        event_type: Type of event
        source: Event source information
        data: Event data
        
    Returns:
        Response data
    """
    if event_type == 'status_request':
        # Return current bot status
        return {
            'status': 'online',
            'active_positions': len(dashboard_state['active_positions']),
            'total_trades': dashboard_state['analytics'].get('total_trades', 0)
        }
    
    elif event_type == 'command':
        # Handle commands from overseer-bot-ui
        command = data.get('command', '')
        logger.info(f"Received command: {command}")
        
        # Command handling would go here
        return {
            'command': command,
            'result': 'acknowledged',
            'note': 'Command processing not yet implemented'
        }
    
    elif event_type == 'alert':
        # Handle alerts from overseer-bot-ai
        alert_message = data.get('message', 'Alert received')
        dashboard_state['recent_alerts'].insert(0, {
            'type': 'external_alert',
            'message': alert_message,
            'severity': data.get('severity', 'info'),
            'timestamp': datetime.now().isoformat()
        })
        
        return {'result': 'alert_stored'}
    
    else:
        return {'result': 'event_received', 'note': f'Event type {event_type} logged'}


def _calculate_uptime() -> int:
    """Calculate bot uptime in seconds"""
    # This would track actual start time in production
    # For now, return a placeholder
    return 0


# HTML template (embedded for simplicity)
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Token Scalper - Monitoring Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #0a0e27;
            color: #e0e0e0;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            background: #10b981;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: #1a1f3a;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            border: 1px solid #2d3561;
        }
        
        .card h2 {
            font-size: 1.3em;
            margin-bottom: 15px;
            color: #667eea;
        }
        
        .stat {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #2d3561;
        }
        
        .stat:last-child {
            border-bottom: none;
        }
        
        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #10b981;
        }
        
        .alert {
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid;
        }
        
        .alert-warning {
            background: rgba(245, 158, 11, 0.1);
            border-color: #f59e0b;
        }
        
        .alert-danger {
            background: rgba(239, 68, 68, 0.1);
            border-color: #ef4444;
        }
        
        .alert-success {
            background: rgba(16, 185, 129, 0.1);
            border-color: #10b981;
        }
        
        .alert-info {
            background: rgba(59, 130, 246, 0.1);
            border-color: #3b82f6;
        }
        
        .timestamp {
            font-size: 0.85em;
            color: #9ca3af;
        }
        
        .position-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .position-item {
            background: #0f1425;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 3px solid #667eea;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #9ca3af;
        }
        
        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            margin: 10px 0;
        }
        
        .refresh-btn:hover {
            background: #5568d3;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Token Scalper - Monitoring Dashboard</h1>
        <span class="status-badge" id="status">● ONLINE</span>
        <p style="margin-top: 10px; opacity: 0.9;">Real-time monitoring and analytics</p>
    </div>
    
    <div class="dashboard-grid">
        <div class="card">
            <h2>📊 Analytics</h2>
            <div class="stat">
                <span>Total Trades</span>
                <span class="stat-value" id="total-trades">0</span>
            </div>
            <div class="stat">
                <span>Successful Trades</span>
                <span class="stat-value" id="successful-trades">0</span>
            </div>
            <div class="stat">
                <span>Rug Pulls Avoided</span>
                <span class="stat-value" id="rugs-avoided">0</span>
            </div>
            <div class="stat">
                <span>Total Profit</span>
                <span class="stat-value" id="total-profit">$0</span>
            </div>
        </div>
        
        <div class="card">
            <h2>👥 Developer Tracking</h2>
            <div class="stat">
                <span>Tracked Developers</span>
                <span class="stat-value" id="tracked-devs">0</span>
            </div>
            <div class="stat">
                <span>Flagged Developers</span>
                <span class="stat-value" id="flagged-devs" style="color: #ef4444;">0</span>
            </div>
            <div class="stat">
                <span>Tracked Projects</span>
                <span class="stat-value" id="tracked-projects">0</span>
            </div>
            <div class="stat">
                <span>Rugged Projects</span>
                <span class="stat-value" id="rugged-projects" style="color: #ef4444;">0</span>
            </div>
        </div>
        
        <div class="card">
            <h2>💼 Active Positions</h2>
            <button class="refresh-btn" onclick="refreshData()">Refresh</button>
            <div class="position-list" id="positions-list">
                <div class="loading">Loading positions...</div>
            </div>
        </div>
    </div>
    
    <div class="card">
        <h2>🔔 Recent Alerts</h2>
        <button class="refresh-btn" onclick="refreshAlerts()">Refresh Alerts</button>
        <div id="alerts-list">
            <div class="loading">Loading alerts...</div>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 5 seconds
        setInterval(refreshData, 5000);
        
        // Initial load
        refreshData();
        
        function refreshData() {
            fetchAnalytics();
            fetchDeveloperStats();
            fetchPositions();
            fetchAlerts();
        }
        
        function fetchAnalytics() {
            fetch('/api/analytics')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('total-trades').textContent = data.total_trades || 0;
                    document.getElementById('successful-trades').textContent = data.successful_trades || 0;
                    document.getElementById('rugs-avoided').textContent = data.rug_pulls_avoided || 0;
                    document.getElementById('total-profit').textContent = '$' + (data.total_profit_usd || 0).toFixed(2);
                })
                .catch(error => console.error('Error fetching analytics:', error));
        }
        
        function fetchDeveloperStats() {
            fetch('/api/developer-stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('tracked-devs').textContent = data.total_developers || 0;
                    document.getElementById('flagged-devs').textContent = data.scam_developers || 0;
                    document.getElementById('tracked-projects').textContent = data.total_projects || 0;
                    document.getElementById('rugged-projects').textContent = data.rugged_projects || 0;
                })
                .catch(error => console.error('Error fetching developer stats:', error));
        }
        
        function fetchPositions() {
            fetch('/api/positions')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('positions-list');
                    if (data.length === 0) {
                        container.innerHTML = '<div class="loading">No active positions</div>';
                    } else {
                        container.innerHTML = data.map(pos => `
                            <div class="position-item">
                                <strong>${pos.token_name || 'Unknown'}</strong><br>
                                <span class="timestamp">${pos.token_address || 'N/A'}</span><br>
                                Profit/Loss: <span style="color: ${pos.profit >= 0 ? '#10b981' : '#ef4444'}">${pos.profit_percent || 0}%</span>
                            </div>
                        `).join('');
                    }
                })
                .catch(error => {
                    console.error('Error fetching positions:', error);
                    document.getElementById('positions-list').innerHTML = '<div class="loading">Error loading positions</div>';
                });
        }
        
        function fetchAlerts() {
            fetch('/api/alerts?limit=10')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('alerts-list');
                    if (data.length === 0) {
                        container.innerHTML = '<div class="loading">No recent alerts</div>';
                    } else {
                        container.innerHTML = data.map(alert => {
                            const severityClass = alert.severity === 'danger' ? 'alert-danger' :
                                                 alert.severity === 'warning' ? 'alert-warning' :
                                                 alert.severity === 'success' ? 'alert-success' : 'alert-info';
                            return `
                                <div class="alert ${severityClass}">
                                    <strong>${alert.type}</strong><br>
                                    ${alert.message}<br>
                                    <span class="timestamp">${new Date(alert.timestamp).toLocaleString()}</span>
                                </div>
                            `;
                        }).join('');
                    }
                })
                .catch(error => {
                    console.error('Error fetching alerts:', error);
                    document.getElementById('alerts-list').innerHTML = '<div class="loading">Error loading alerts</div>';
                });
        }
        
        function refreshAlerts() {
            fetchAlerts();
        }
    </script>
</body>
</html>
'''


# Save the HTML template
def save_dashboard_template():
    """Save dashboard HTML template to templates directory"""
    import os
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    with open('templates/dashboard.html', 'w') as f:
        f.write(DASHBOARD_HTML)
    
    logger.info("Dashboard template saved to templates/dashboard.html")


# Initialize template on module load
try:
    save_dashboard_template()
except Exception as e:
    logger.warning(f"Could not save dashboard template: {e}")
