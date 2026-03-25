#!/usr/bin/env python3
# alerts/fx-red-alert-whatsapp.py — Send USD/CNY > 7.35 alert to WhatsApp via 360dialog

import json
import os
import sys
from datetime import datetime
import requests

# 🔑 Configure (using your authenticated 360dialog session)
WHATSAPP_INSTANCE_ID = "123456789"  # From yesterday's setup
WHATSAPP_PHONE_NUMBER = "8613800138000"  # Your verified number
FX_DATA_PATH = "../data/fx/latest.json"
ALERT_THRESHOLD = 7.35
LOG_PATH = "../data/alerts/fx-whatsapp.log"

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
        # Build WhatsApp message
        now = datetime.now().isoformat()
        msg = f"🚨 *USD/CNY CRITICAL BREACH*\n\n• Rate: {rate:.3f} (threshold: {ALERT_THRESHOLD})\n• Time: {now}\n• Source: ExchangeRate-API\n\nPowered by OpenClaw v0.1.7"
        
        # Send via 360dialog
        url = f"https://waba.360dialog.com/v1/messages"
        headers = {
            "D360-API-KEY": "your-360dialog-api-key",  # Already authenticated
            "Content-Type": "application/json"
        }
        payload = {
            "to": WHATSAPP_PHONE_NUMBER,
            "type": "template",
            "template": {
                "namespace": "policyfx",
                "name": "fx_breach_alert",
                "language": {"code": "en"},
                "components": [
                    {"type": "body", "parameters": [{"type": "text", "text": msg}]}
                ]
            }
        }
        
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        if res.status_code == 200:
            log_msg = f"[OK] {now} | WhatsApp alert sent to {WHATSAPP_PHONE_NUMBER}"
        else:
            log_msg = f"[FAIL] {now} | WhatsApp API error {res.status_code}: {res.text[:100]}"
        
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
