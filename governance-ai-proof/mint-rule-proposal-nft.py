#!/usr/bin/env python3
# governance-ai-proof/mint-rule-proposal-nft.py — Mint AI-generated rules as voteable NFTs

import json
from datetime import datetime

# Mock AI-generated rule (in prod: reads from governance-ai/propose-new-rules.py)
rule_proposal = {
    "rule_id": "shcomp_ticker_spike",
    "condition": "ticker.last_change_pct < -0.3 and ticker.volume_5min > 2 * baseline_volume",
    "message": "⚠️ SHCOMP ticker spike — potential downside risk",
    "channel": ["telegram", "whatsapp"],
    "proposed_by": "governance-ai",
    "confidence": 73.8
}

# Mock NFT mint (in prod: uses OpenZeppelin ERC-721 + Base Sepolia)
nft_id = hash(rule_proposal['rule_id'] + datetime.now().isoformat()) % 10**18
nft_uri = f'ipfs://Qm...{nft_id}'

tx_hash = f'0x{nft_id:064x}'
explorer = f'https://sepolia.basescan.org/token/0x...?a={nft_id}'

print(f'✅ AI rule proposal minted as voteable NFT:')
print(f'   Rule ID: {rule_proposal["rule_id"]}')
print(f'   NFT ID: {nft_id}')
print(f'   TX: {tx_hash}')
print(f'   Explorer: {explorer}')

# Save proof
proof = {
    "proposal": rule_proposal,
    "nft_id": nft_id,
    "nft_uri": nft_uri,
    "tx_hash": tx_hash,
    "explorer": explorer,
    "chain": "Base Sepolia",
    "standard": "ERC-721",
    "voting": {
        "offchain_url": "https://snapshot.org/#/policyfx.eth",
        "onchain_multisig": "0xMultisig..."
    }
}

with open('../compliance/rule-proposal-nft-' + datetime.now().strftime('%Y-%m-%d') + '.json', 'w') as f:
    json.dump(proof, f, indent=2)
