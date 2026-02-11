#!/usr/bin/env python3
"""
Test script for ecosystem integration and webhook endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"
API_KEY = "test_api_key_12345"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing /api/status/health...")
    try:
        response = requests.get(f"{BASE_URL}/status/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed")
            print(f"   Status: {data['status']}")
            print(f"   Bot ID: {data['bot_id']}")
            print(f"   Version: {data['version']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_metrics_endpoint():
    """Test the metrics endpoint"""
    print("\nTesting /api/status/metrics...")
    try:
        response = requests.get(f"{BASE_URL}/status/metrics")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Metrics endpoint passed")
            print(f"   Total Trades: {data['token_scalper_total_trades']}")
            print(f"   Active Positions: {data['token_scalper_active_positions']}")
            return True
        else:
            print(f"❌ Metrics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_webhook_event():
    """Test receiving a webhook event"""
    print("\nTesting /api/webhook/event...")
    
    event = {
        "event_id": "test-001",
        "event_type": "status_request",
        "source": {
            "bot_id": "test-bot",
            "bot_name": "Test Bot",
            "bot_type": "test"
        },
        "timestamp": datetime.now().isoformat(),
        "priority": "normal",
        "data": {}
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/webhook/event", json=event, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook event passed")
            print(f"   Status: {data['status']}")
            print(f"   Event ID: {data['event_id']}")
            print(f"   Response: {data.get('response', {})}")
            return True
        else:
            print(f"❌ Webhook event failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_webhook_heartbeat():
    """Test receiving a heartbeat"""
    print("\nTesting /api/webhook/heartbeat...")
    
    heartbeat = {
        "bot_id": "test-bot",
        "bot_name": "Test Bot",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": 3600
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/webhook/heartbeat", json=heartbeat, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Heartbeat passed")
            print(f"   Status: {data['status']}")
            return True
        else:
            print(f"❌ Heartbeat failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Ecosystem Integration & Webhook Endpoint Tests")
    print("=" * 60)
    print("\nNote: Dashboard must be running on http://localhost:5000")
    print("Start it with: python -c 'from monitoring_dashboard import app; app.run()'")
    print()
    
    results = []
    
    # Test public endpoints
    results.append(test_health_endpoint())
    results.append(test_metrics_endpoint())
    
    # Test webhook endpoints
    results.append(test_webhook_event())
    results.append(test_webhook_heartbeat())
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
