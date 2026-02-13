# Render.com Deployment Quick Reference

This is a quick reference guide for deploying Token Scalper Bot to Render.com.

## 🚨 Common Error Fix

If you see this error:
```
ImportError: Failed to find application, did you mean 'main:application'?
```

**Cause:** Render is running `gunicorn main.py` instead of `gunicorn wsgi:application`

**Quick Fix:** Go to your service settings in Render Dashboard and either:
1. **Clear the "Start Command" field** (leave it blank), OR
2. Set it to: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - --log-level info wsgi:application`

See [Full Troubleshooting Guide](DEPLOYMENT.md#troubleshooting)

## ✅ Recommended Deployment Method

### Option 1: Blueprint (Infrastructure as Code) - BEST

This ensures Render always uses the configuration from the repository:

1. In Render Dashboard: **New → Blueprint**
2. Connect your GitHub repository
3. Render detects `render.yaml` and shows the plan
4. Add your environment variables
5. Click **"Apply"**

✅ Benefits:
- Configuration is version-controlled in Git
- No manual dashboard configuration needed
- Automatically redeploys on YAML changes
- Can't be overridden by dashboard settings

### Option 2: Regular Web Service with Procfile

1. Create a **Web Service** (not Blueprint)
2. Connect your GitHub repository
3. **IMPORTANT:** Leave the "Start Command" field **EMPTY**
4. Render will use the command from `Procfile`
5. Add environment variables
6. Deploy

⚠️ The "Start Command" field MUST be empty for this to work!

## 📋 Configuration Files

All these files are already in the repository and correctly configured:

- ✅ `render.yaml` - Blueprint configuration
- ✅ `Procfile` - Start command for non-Blueprint deployments
- ✅ `wsgi.py` - WSGI entry point for Gunicorn
- ✅ `runtime.txt` - Python version specification
- ✅ `build.sh` - Build script
- ✅ `requirements.txt` - Python dependencies

## 🔧 Correct Commands

These commands are already configured in the repository:

**Build Command:**
```bash
./build.sh
```

**Start Command:**
```bash
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - --log-level info wsgi:application
```

## 🌍 Required Environment Variables

Add these in the Render Dashboard:

**Essential:**
- `PORT` - (Auto-set by Render, don't add manually)
- `FLASK_SECRET_KEY` - Your secret key for Flask sessions

**Optional (Trading Features):**
- `SOLANA_RPC_URL` - Your Solana RPC endpoint
- `SOLANA_PRIVATE_KEY` - Your wallet private key
- `EVM_PRIVATE_KEY` - Your EVM wallet private key
- `INFURA_KEY` - Infura API key
- `ALCHEMY_KEY` - Alchemy API key

**Optional (Integrations):**
- `ECOSYSTEM_BOT_ID` - Bot ID for ecosystem integration
- `ECOSYSTEM_API_KEY` - API key for webhooks
- `TWITTER_API_KEY` - Twitter API key
- `TWITTER_API_SECRET` - Twitter API secret

See [complete list in DEPLOYMENT.md](DEPLOYMENT.md)

## 📚 More Information

- **[Full Deployment Guide](DEPLOYMENT.md)** - Complete instructions for all platforms
- **[Main README](README.md)** - Bot features and usage
- **[Troubleshooting](DEPLOYMENT.md#troubleshooting)** - Solutions for common issues

## 🆘 Still Having Issues?

1. Check the [Troubleshooting section](DEPLOYMENT.md#troubleshooting) in DEPLOYMENT.md
2. Verify all configuration files are committed to your repository
3. Ensure you're using the Blueprint deployment method
4. Check that the "Start Command" field in Render Dashboard is either empty or has the correct command

The repository configuration is correct - the issue is usually in how the Render service was created or configured in the dashboard.
