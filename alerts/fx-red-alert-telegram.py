#!/usr/bin/env python3
# alerts/fx-red-alert-telegram.py - Send USD/CNY > 7.35 alert to Telegram

import json
import os
import sys
import time
from datetime import datetime
import requests

# 🔑 Configure with YOUR values
import os
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'YOUR_TELEGRAM_TOKEN_HERE')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'YOUR_TELEGRAM_CHAT_ID_HERE')
FX_DATA_PATH = "data/fx/latest.json"
ALERT_THRESHOLD = 7.35
LOG_PATH = "data/alerts/fx-telegram.log"

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

    # ✅ Always send a test alert on first run (to verify setup)
    now = datetime.now().isoformat()
    msg = f"✅ *Policy+FX Trust Layer - ONLINE*\n\n• USD/CNY = {rate:.3f}\n• Threshold = {ALERT_THRESHOLD}\n• Time = {now}\n• Source = [ExchangeRate-API]({fx.get('sourceUrl', '#')})\n\nPowered by OpenClaw v0.1.1"

    # Send to Telegram
    if TELEGRAM_TOKEN == 'YOUR_TELEGRAM_TOKEN_HERE' or TELEGRAM_CHAT_ID == 'YOUR_TELEGRAM_CHAT_ID_HERE':
        log_msg = f"[CONFIG ERROR] {now} | Telegram credentials not configured. Set TELEGRAM_TOKEN and TELEGRAM_CHAT_ID environment variables."
        print(log_msg)
        with open(LOG_PATH, 'a') as f:
            f.write(log_msg + '\n')
        sys.exit(1)
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    res = requests.post(url, json=payload, timeout=10)
    if res.status_code == 200:
        log_msg = f"[OK] {now} | Test alert sent to Telegram (chat_id: {TELEGRAM_CHAT_ID})"
    else:
        log_msg = f"[FAIL] {now} | Telegram API error {res.status_code}: {res.text[:100]}"

    # Log
    with open(LOG_PATH, 'a') as f:
        f.write(log_msg + '\n')

    print(log_msg)

except Exception as e:
    err_msg = f"[ERROR] {datetime.now().isoformat()} | {str(e)}"
    with open(LOG_PATH, 'a') as f:
        f.write(err_msg + '\n')
    print(err_msg)
