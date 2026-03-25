#!/usr/bin/env python3
# ai-trading/generate-signal.py — AI-powered trade signal engine

import json
from datetime import datetime

# Load live data
try:
    with open('../data/fx/latest.json') as f:
        fx = json.load(f)
    with open('../data/policy/latest.json') as f:
        policy = json.load(f)
    with open('../data/shanghai/latest.json') as f:
        shcomp = json.load(f)
except Exception as e:
    print(f'❌ Error loading data: {e}')
    fx = {'rate': 6.9}
    policy = {'latestValid': {'title': 'No RRR cut today'}}
    shcomp = {'index': 3025.4}

# Your A股 Decision Framework logic
signal = None
reason = ''
confidence = 0

if (fx.get('rate', 0) <= 7.20 and 
    policy.get('latestValid') and '下调' in policy['latestValid'].get('title', '') and 
    shcomp.get('index', 0) > 2900):
    signal = 'BUY_CNY_BONDS'
    reason = 'PBOC RRR cut confirmed + SHCOMP > 2900 + USD/CNY ≤ 7.20'
    confidence = 92
elif fx.get('rate', 0) > 7.35:
    signal = 'HEDGE_USD'
    reason = 'USD/CNY breach > 7.35 → hedge FX exposure'
    confidence = 88
else:
    signal = 'HOLD'
    reason = 'No clear catalyst — monitor PBOC & FX'
    confidence = 65

# Build output
output = {
    "generated_at": datetime.now().isoformat(),
    "signal": signal,
    "confidence": confidence,
    "reason": reason,
    "execution": "Execute via ICBC bond desk before 15:00 CST" if signal == 'BUY_CNY_BONDS' else "Monitor next PBOC announcement"
}

# Save
filename = f'reports/trade-signal-{datetime.now().strftime("%Y-%m-%d")}.json'
import os
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, 'w') as f:
    json.dump(output, f, indent=2)

print(f'✅ Trade signal generated: {filename}')
print(json.dumps(output, indent=2))
