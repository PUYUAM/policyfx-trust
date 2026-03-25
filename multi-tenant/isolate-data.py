#!/usr/bin/env python3
# multi-tenant/isolate-data.py — Create tenant-isolated data directories

import os
import sys
import json

if len(sys.argv) < 2:
    print('Usage: python3 isolate-data.py <tenant-id>')
    sys.exit(1)

tenant_id = sys.argv[1]
dir_path = f'data/{tenant_id}'

# Create isolated structure
os.makedirs(f'{dir_path}/fx', exist_ok=True)
os.makedirs(f'{dir_path}/policy', exist_ok=True)
os.makedirs(f'{dir_path}/shanghai', exist_ok=True)
os.makedirs(f'{dir_path}/alerts', exist_ok=True)
os.makedirs(f'{dir_path}/analytics', exist_ok=True)

# Write config
config = {
    "tenant_id": tenant_id,
    "branding": {
        "name": f"{tenant_id.title()} Financial Trust",
        "logo": f"/ui/branding/{tenant_id}/logo.png",
        "color": "#3498db"
    },
    "rbac": {
        "admin": ["read", "write", "delete"],
        "analyst": ["read", "write"],
        "viewer": ["read"]
    }
}

with open(f'{dir_path}/config.json', 'w') as f:
    json.dump(config, f, indent=2)

print(f'✅ Tenant {tenant_id} isolated at {dir_path}')
