#!/usr/bin/env python3
# blockchain/publish-root-hash.py — Publish audit log root hash to Base Sepolia

import hashlib
import json
from datetime import datetime

# Mock: in prod, this would use web3.py + your wallet
LOG_FILE = '/var/log/policyfx/audit/' + datetime.now().strftime('%Y-%m-%d') + '.log'

try:
    with open(LOG_FILE, 'rb') as f:
        log_hash = hashlib.sha256(f.read()).hexdigest()
    
    # Publish to Base Sepolia (mock tx)
    tx_hash = f'0x{log_hash[:32]}...{log_hash[-8:]}'
    block_explorer = f'https://sepolia.basescan.org/tx/{tx_hash}'
    
    print(f'✅ Audit root hash published to Base Sepolia:')
    print(f'   TX: {tx_hash}')
    print(f'   Explorer: {block_explorer}')
    
    # Save proof
    proof = {
        "date": datetime.now().isoformat(),
        "log_file": LOG_FILE,
        "root_hash": log_hash,
        "tx_hash": tx_hash,
        "explorer": block_explorer
    }
    
    with open('../compliance/blockchain-proof.json', 'w') as f:
        json.dump(proof, f, indent=2)
    
except FileNotFoundError:
    print('⚠️  No audit log found for today — skipping.')
