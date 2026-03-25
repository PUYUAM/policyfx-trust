#!/usr/bin/env python3
# alerts/fx-red-alert.py — Fire Slack alert when USD/CNY breaches 7.35

import json
import os
import sys
import time
import logging
from datetime import datetime
import requests

# Configure
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/HERE"  # ← REPLACE
FX_DATA_PATH = "data/fx/latest.json"
ALERT_THRESHOLD = 7.35
LOG_PATH = "data/alerts/fx-red.log"

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

if not os.path.exists(FX_DATA_PATH):
    print(f"⚠️  {FX_DATA_PATH} not found. Skipping.")
    sys.exit(0)

try:
    with open(FX_DATA_PATH, 'r') as f:
        fx = json.load(f)
    
    if 'rate' not in fx:
        print(f"⚠️  No 'rate' in {FX_DATA_PATH}")
        sys.exit(0)
    
    rate = float(fx['rate'])
    
    if rate > ALERT_THRESHOLD:
        # Build alert
        now = datetime.now().isoformat()
        msg = {
            "text": f"🚨 *USD/CNY CRITICAL BREACH*",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Rate:* {rate:.3f} (threshold: {ALERT_THRESHOLD})\n*Time:* {now}\n*Source:* <{fx.get('sourceUrl', '#')|PBOC/ExchangeRate-API>"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "Powered by OpenClaw Policy+FX Trust Layer v0.1"
                        }
                    ]
                }
            ]
        }
        
        # Send
        res = requests.post(SLACK_WEBHOOK_URL, json=msg, timeout=10)
        if res.status_code == 200:
            log_msg = f"[OK] {now} | {rate:.3f} > {ALERT_THRESHOLD} → Slack alert sent"
        else:
            log_msg = f"[FAIL] {now} | Slack API error {res.status_code}: {res.text[:100]}"
        
        # Log
        with open(LOG_PATH, 'a') as f:
            f.write(log_msg + '\n')
        
        print(log_msg)
    else:
        print(f"✅ OK: {rate:.3f} ≤ {ALERT_THRESHOLD}")
        
except Exception as e:
    err_msg = f"[ERROR] {datetime.now().isoformat()} | {str(e)}"
    with open(LOG_PATH, 'a') as f:
        f.write(err_msg + '\n')
    print(err_msg)
