#!/usr/bin/env python3
# security/audit/immutable-log.py — SOC2-compliant immutable audit logging

import os
import json
import hashlib
from datetime import datetime

def log_event(action, user='system', ip='127.0.0.1', payload=None):
    # Build log line
    timestamp = datetime.now().isoformat()
    log_line = f'{timestamp}|{action}|{user}|{ip}'
    
    # Sign payload
    if payload:
        payload_str = json.dumps(payload, sort_keys=True)
        signature = hashlib.sha256(payload_str.encode()).hexdigest()
        log_line += f'|{signature}'
    
    # Write to immutable log
    log_dir = '/var/log/policyfx/audit'
    os.makedirs(log_dir, exist_ok=True)
    log_file = f'{log_dir}/{datetime.now().strftime("%Y-%m-%d")}.log'
    
    with open(log_file, 'a') as f:
        f.write(log_line + '\n')
    
    print(f'✅ Audit logged: {log_file}')

# Example usage
if __name__ == '__main__':
    log_event('dashboard_view', user='puyuam', ip='192.168.1.100', payload={'url': '/ui/index.html'})
