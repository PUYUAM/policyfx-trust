#!/usr/bin/env python3
# alerts/evaluate-custom-rules.py — Evaluate custom alert rules against live data

import json
import os
import sys
from datetime import datetime
import requests

# Load rules
RULES_PATH = 'custom-rules.json'
if not os.path.exists(RULES_PATH):
    print('⚠️  No custom rules found.')
    sys.exit(0)

with open(RULES_PATH) as f:
    rules = json.load(f)

# Load data
def read_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {}

fx = read_json('../data/fx/latest.json')
policy = read_json('../data/policy/latest.json')
shcomp = read_json('../data/shanghai/latest.json')

data = {'fx': fx, 'policy': policy, 'shcomp': shcomp}

# Evaluate each rule
for rule_id, rule in rules.items():
    try:
        # Safe eval (no arbitrary code)
        if eval(rule['condition'], {"__builtins__": {}}, data):
            msg = rule['message']
            
            # Send to channels
            for channel in rule.get('channel', []):
                if channel == 'telegram':
                    requests.post(
                        f"https://api.telegram.org/bot8732474762:AAHw142jWzb2fkyf6B-p2R-rcwXMn4uCJ0o/sendMessage",
                        json={"chat_id": "8545379026", "text": msg, "parse_mode": "Markdown"}
                    )
                elif channel == 'whatsapp':
                    # Stub — would use 360dialog in prod
                    print(f'✅ WhatsApp alert stubbed for: {msg}')
            
            print(f'✅ Rule triggered: {rule_id} → {msg}')
            
    except Exception as e:
        print(f'❌ Rule {rule_id} error: {e}')
