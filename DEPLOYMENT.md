# Deployment Guide

> **🚨 Quick Fix:** If you're seeing `ImportError: Failed to find application` or Render is running `gunicorn main.py`, jump to the [Troubleshooting section](#troubleshooting) for immediate solutions.

## Overview

Token Scalper Bot can be deployed as a web service to cloud platforms like Render, Heroku, Railway, or any container-based hosting. The bot automatically detects deployment environments and starts a monitoring dashboard web server.

## Quick Start

### Automatic Detection (Recommended)

The bot automatically starts in web service mode when the `PORT` environment variable is set:

```bash
# Render, Heroku, Railway all set PORT automatically
python main.py
# Output: Detected PORT environment variable - running in web service mode
```

### Manual Web Service Mode

You can explicitly start the web service:

```bash
# Start web service with default config
python main.py web

# Start with custom config
python main.py --config production-config.json web
```

## Deployment Platforms

### Render.com

> **⚠️ IMPORTANT:** If you see the error "ImportError: Failed to find application, did you mean 'main:application'?" or Render is running `gunicorn main.py`, your service has a manual Start Command in the dashboard that's overriding the repository configuration. See the [Troubleshooting](#troubleshooting) section below for solutions.

**Setup:**

**Option 1: Using Blueprint (Infrastructure as Code) - MOST RELIABLE**

This option ensures Render always uses the configuration from your repository:

1. In Render Dashboard, click **"New" → "Blueprint"**
2. Connect your GitHub repository and select the branch
3. Render will detect the `render.yaml` file and show you the deployment plan
4. Add your environment variables (see below)
5. Click "Apply" to deploy

This method prevents Render from auto-detecting and using incorrect commands. The `render.yaml` file defines:
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - --log-level info wsgi:application`

**Option 2: Using Procfile with Regular Web Service**

The repository includes a `Procfile` that specifies the start command:

1. Create a new **Web Service** (not Blueprint)
2. Connect your GitHub repository
3. In the service settings, ensure the **"Start Command" field is EMPTY** (leave it blank)
4. Render will use the command from the Procfile
5. Add environment variables (see below)
6. Deploy

**Note:** If the "Start Command" field has any value (e.g., `gunicorn main.py`), it will override the Procfile. You must clear this field.

**Option 3: Manual Configuration (If Options 1 & 2 Don't Work)**

Only use this if the above options don't work or if you need custom settings:

1. Create a new Web Service
2. Connect your GitHub repository
3. Manually configure build and start commands in the dashboard:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - --log-level info wsgi:application`
4. Add environment variables (see below)
5. Deploy

**Note:** Manual configuration in the dashboard will override both `render.yaml` and `Procfile`. Use Option 1 (Blueprint) or Option 2 (Procfile) for easier maintenance.

Render automatically sets the `PORT` environment variable, which the bot uses to:
- Bind to the correct port
- Start the monitoring dashboard

### Heroku

**Setup:**
1. Create a new app
2. Add Python buildpack
3. Deploy via Git or GitHub integration
4. The repository includes a `Procfile` with the recommended Gunicorn command:
   ```
   web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - --log-level info wsgi:application
   ```
   Alternative: You can modify the Procfile to use the Python wrapper:
   ```
   web: python main.py
   ```
5. Add environment variables via Config Vars

### Railway

**Setup:**
1. Create new project from GitHub repo
2. Railway auto-detects Python and runs `python main.py`
3. Add environment variables
4. Deploy

### Docker

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Expose port (override with PORT env var)
EXPOSE 5000

# Start in web service mode
CMD ["python", "main.py", "web"]
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  token-scalper:
    build: .
    ports:
      - "5000:5000"
    environment:
      - PORT=5000
      - FLASK_SECRET_KEY=your-secret-key
    env_file:
      - .env
```

## Environment Variables

### Required for Web Service

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Port for web server (auto-set by platforms) | 5000 |

### Optional

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_SECRET_KEY` | Flask session secret | `random-secret-key-123` |
| `USE_GUNICORN` | Use Gunicorn server (default: true). Accepts: true/1/yes or false/0/no | `true` |
| `WEB_CONCURRENCY` | Number of Gunicorn workers | `4` |
| `GUNICORN_TIMEOUT` | Worker timeout in seconds (default: 120) | `180` |
| `ECOSYSTEM_API_KEY` | API key for webhook auth | `your-api-key` |
| `ECOSYSTEM_SHARED_SECRET` | Shared secret for webhooks | `shared-secret-456` |

### Bot Configuration (Optional)

You can configure the bot using environment variables or a config file. See `.env.example` for all available options.

## Configuration Files

### Minimal Deployment Config

Create `config.deployment.json`:

```json
{
  "dashboard": {
    "enabled": true,
    "host": "0.0.0.0",
    "port": 5000
  },
  "monitoring": {
    "scan_interval_seconds": 60
  }
}
```

Use it with:
```bash
python main.py --config config.deployment.json web
```

### Full Config

See `config.example.json` for all configuration options including:
- Wallet configuration
- Trading parameters
- Safety features
- AI analysis
- Social media integration
- Ecosystem webhooks

## Dashboard Access

Once deployed, the dashboard provides:

- **Real-time Monitoring:** View active positions and wallet balances
- **Alerts:** See recent alerts and notifications
- **Analytics:** Track performance metrics
- **Developer Stats:** Monitor developer reputation scores
- **API Endpoints:** 
  - `/api/status` - Bot status
  - `/api/positions` - Current positions
  - `/api/wallets` - Wallet information
  - `/api/alerts` - Recent alerts
  - `/api/webhook/event` - Receive webhook events
  - `/api/webhook/heartbeat` - Heartbeat endpoint

## Port Binding

The bot binds to `0.0.0.0` in web service mode, making it accessible from external connections. The port is determined by:

1. `PORT` environment variable (highest priority)
2. Config file `dashboard.port` setting
3. Default: 5000

## Health Checks

Use the `/api/status/health` endpoint for platform health checks:

```bash
curl http://your-app.com/api/status/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-12T23:55:00Z",
  "uptime_seconds": 3600,
  "version": "1.0.0"
}
```

## Troubleshooting

### "Failed to find application" or "ImportError: Failed to find application, did you mean 'main:application'?"

**Error in logs:**
```
Running 'gunicorn main.py'
ImportError: Failed to find application, did you mean 'main:application'?
```

**Root Cause:** Render is running `gunicorn main.py` instead of the correct `gunicorn wsgi:application` command. This happens when:
1. The service was created as a regular Web Service (not via Blueprint)
2. The "Start Command" field in the dashboard has a value that overrides the repository configuration
3. Render's auto-detection picked the wrong command

**Solutions (in order of preference):**

**Solution 1: Deploy as Blueprint (Best Solution)**
1. Delete the existing service or leave it
2. In Render Dashboard: **New → Blueprint**
3. Connect your GitHub repository
4. Render will detect the `render.yaml` file
5. Review the plan and click "Apply"

This ensures Render always uses the configuration from `render.yaml` in the repository.

**Solution 2: Clear the Dashboard Start Command**
1. Go to your service in the Render Dashboard
2. Navigate to **Settings**
3. Find the **"Start Command"** field
4. **Clear it completely** (leave it blank/empty)
5. Scroll down and click **"Save Changes"**
6. Manually trigger a redeploy

This allows Render to use the command from the `Procfile` in the repository.

**Solution 3: Manually Set the Correct Command**
1. Go to your service settings in the Render Dashboard
2. Set **"Start Command"** to exactly:
   ```
   gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - --log-level info wsgi:application
   ```
3. Ensure **"Build Command"** is: `./build.sh`
4. Save and redeploy

**Important Notes:**
- The command must use `wsgi:application` (module:callable format), **NOT** `main.py` or `wsgi.py` (file paths)
- Dashboard settings override both `render.yaml` and `Procfile`
- Both `render.yaml` and `Procfile` in this repository are already correct - the issue is in the Render Dashboard configuration

### "Application exited early"

**Cause:** Bot is not detecting deployment environment and is exiting after showing help.

**Solution:** Ensure the `PORT` environment variable is set, or use explicit `web` command:
```bash
python main.py web
```

### "No open ports detected"

**Cause:** Bot is not binding to a port or is binding to `127.0.0.1`.

**Solution:** The bot automatically binds to `0.0.0.0` in web service mode. Verify:
1. `PORT` environment variable is set
2. Bot logs show `Running on all addresses (0.0.0.0)`

### Connection refused

**Cause:** Firewall or incorrect port configuration.

**Solution:**
1. Check platform logs for actual port
2. Verify `PORT` environment variable matches expected port
3. Ensure platform firewall allows inbound connections

## Production Considerations

### WSGI Server

**✅ Production-ready by default!** The bot now uses Gunicorn automatically in web service mode for better performance and security.

**How it works:**
- Gunicorn is enabled by default (USE_GUNICORN=true)
- When in web service mode (PORT set or `python main.py web`), Gunicorn starts automatically
- Worker count is automatically calculated based on available CPU cores
- Falls back to Flask development server only if `USE_GUNICORN=false` is explicitly set

**Configuration:**

The bot uses optimal defaults, but you can customize:

```bash
# Control worker count (default: auto-calculated from CPU cores)
WEB_CONCURRENCY=4 python main.py

# Disable Gunicorn - forces Flask dev server (not recommended for production)
USE_GUNICORN=false python main.py

# Custom timeout for long-running requests (default: 120 seconds)
GUNICORN_TIMEOUT=180 python main.py
```

**Manual Gunicorn usage (advanced):**

If you need direct control over Gunicorn:

```bash
# Install dependencies
pip install -r requirements.txt

# Run with custom Gunicorn settings
gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 wsgi:application
```

### Security

1. **Set FLASK_SECRET_KEY:** Use a strong random secret
2. **Use HTTPS:** Enable SSL/TLS on your platform
3. **Environment Variables:** Never commit secrets to Git
4. **Webhook Auth:** Enable API key authentication for webhooks
5. **Private Keys:** Store wallet keys in environment variables, not config files

### Monitoring

- Use platform logs to monitor application health
- Set up alerts for errors or crashes
- Monitor memory and CPU usage
- Use dashboard `/api/status/health` for uptime monitoring

## CLI vs Web Service

### CLI Mode (Local Development)

```bash
# Show help
python main.py --help

# Run trading bot locally
python main.py run

# Search for airdrops
python main.py airdrops

# Generate wallets
python main.py genwallets
```

### Web Service Mode (Deployment)

```bash
# Auto-detect (PORT set)
python main.py

# Explicit web service
python main.py web
```

## Examples

### Development

```bash
# Local testing
python main.py web

# Access dashboard
curl http://localhost:5000
```

### Staging/Production

```bash
# Platform sets PORT automatically
# Just run: python main.py

# Or explicitly:
PORT=10000 python main.py
```

## Support

For issues or questions:
- Check platform logs first
- Review this deployment guide
- See [README.md](README.md) for general documentation
- See [ECOSYSTEM_SETUP.md](ECOSYSTEM_SETUP.md) for multi-bot setup
- See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
