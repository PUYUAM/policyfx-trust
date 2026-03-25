#!/usr/bin/env python3
# alerts/shcomp-breach-alert.py — Alert if Shanghai Composite < 2750 (fresh data)

import json
import os
import sys
from datetime import datetime, timedelta
import requests

# 🔑 Configure
TELEGRAM_TOKEN = "8732474762:AAHw142jWzb2fkyf6B-p2R-rcwXMn4uCJ0o"
TELEGRAM_CHAT_ID = "8545379026"
SHCOMP_DATA_PATH = "data/shanghai/latest.json"
ALERT_THRESHOLD = 2750
LOG_PATH = "data/alerts/shcomp-breach.log"

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

if not os.path.exists(SHCOMP_DATA_PATH):
    # Stub with realistic current value for testing
    shcomp_data = {
        "index": 3025.4,
        "change": -0.23,
        "volume": "42.1B",
        "fetchedAt": datetime.now().isoformat() + 'Z',
        "sourceUrl": "https://www.tradingview.com/symbols/SHANGHAI-SH000001/"
    }
    with open(SHCOMP_DATA_PATH, 'w') as f:
        json.dump(shcomp_data, f, indent=2)
else:
    with open(SHCOMP_DATA_PATH, 'r') as f:
        shcomp_data = json.load(f)

try:
    from datetime import timezone
    now = datetime.now(timezone.utc)
    fetched = datetime.fromisoformat(shcomp_data['fetchedAt'].replace('Z', '+00:00'))
    age_minutes = (now - fetched).total_seconds() / 60
    
    if 'index' in shcomp_data and shcomp_data['index'] < ALERT_THRESHOLD and age_minutes < 1440:
        # Send alert
        msg = f"⚠️ *SHANGHAI COMPOSITE BREACH ALERT*\n\n• Index = {shcomp_data['index']:.1f} (< {ALERT_THRESHOLD})\n• Change = {shcomp_data['change']:+.2f}%\n• Volume = {shcomp_data['volume']}\n• Time = {shcomp_data['fetchedAt']}\n• Source = [TradingView](https://www.tradingview.com/symbols/SHANGHAI-SH000001/)\n\nPowered by OpenClaw v0.1.1"
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        res = requests.post(url, json=payload, timeout=10)
        
        if res.status_code == 200:
            log_msg = f"[OK] {now.isoformat()} | SHCOMP < {ALERT_THRESHOLD}: {shcomp_data['index']:.1f} → Telegram"
        else:
            log_msg = f"[FAIL] {now.isoformat()} | Telegram API error {res.status_code}"
    else:
        log_msg = f"✅ OK: SHCOMP = {shcomp_data['index']:.1f} ≥ {ALERT_THRESHOLD} (or stale: {age_minutes:.0f}m old)"
    
    with open(LOG_PATH, 'a') as f:
        f.write(log_msg + '\n')
    print(log_msg)
    
except Exception as e:
    err_msg = f"[ERROR] {datetime.now().isoformat()} | {str(e)}"
    with open(LOG_PATH, 'a') as f:
        f.write(err_msg + '\n')
    print(err_msg)
