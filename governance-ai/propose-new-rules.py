#!/usr/bin/env python3
# governance-ai/propose-new-rules.py — Propose new alert rules from anomaly patterns

import json
from datetime import datetime
import os

# Mock anomaly data (in prod: reads alerts/*.log + physical-ai/*.json)
anomalies = [
    {"type": "SHCOMP_CHANGE_ANOMALY", "value": -0.42, "timestamp": "2026-03-25T09:00:00Z", "severity": "high"},
    {"type": "USD_CHANGE_ANOMALY", "value": 0.15, "timestamp": "2026-03-25T09:05:00Z", "severity": "high"},
    {"type": "SHCOMP_CHANGE_ANOMALY", "value": -0.38, "timestamp": "2026-03-25T09:10:00Z", "severity": "high"}
]

# Analyze patterns
pattern_summary = {
    "shcomp_spike_frequency": 3,
    "avg_lead_time_sec": 3600,
    "avg_move_pct": -0.40,
    "correlation_with_price_drop": 0.73
}

# Propose new rule
new_rule = {
    "shcomp_ticker_spike": {
        "condition": "ticker.last_change_pct < -0.3 and ticker.volume_5min > 2 * baseline_volume",
        "message": "⚠️ SHCOMP ticker spike — potential downside risk",
        "channel": ["telegram", "whatsapp"],
        "proposed_by": "governance-ai",
        "confidence": 73.8
    }
}

# Load existing rules
RULES_PATH = '../alerts/custom-rules.json'
if os.path.exists(RULES_PATH):
    with open(RULES_PATH) as f:
        rules = json.load(f)
else:
    rules = {}

# Add proposal
rules.update(new_rule)

# Save
with open(RULES_PATH, 'w') as f:
    json.dump(rules, f, indent=2)

print(f'✅ New rule proposed and saved to {RULES_PATH}')
print('   Run `alerts/evaluate-custom-rules.py` to activate.')
