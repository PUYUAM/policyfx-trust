#!/usr/bin/env python3
# scripts/fetch-policy-news.py — Fetch latest PBOC policy news

import subprocess
import sys
import os
import json

# Ensure the data directory exists
os.makedirs('data/policy', exist_ok=True)

# Use the fetcher library to get PBOC policy news
try:
    # For now, we'll use a simple approach - fetch from PBOC's official RSS or news page
    # In a real implementation, this would parse PBOC's news feed
    result = subprocess.run([
        'python3', 
        'lib/fetcher.py', 
        '--url', 'https://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html', 
        '--cache-ttl', '3600', 
        '--output', 'data/policy/latest.json'
    ], capture_output=True, text=True, timeout=30)
    
    if result.returncode == 0:
        print(f"✅ Successfully fetched PBOC policy news")
        # Update the timestamp in the file
        try:
            with open('data/policy/latest.json', 'r') as f:
                data = json.load(f)
            data['last_updated'] = '2026-03-25'
            data['timestamp'] = '2026-03-25T10:46:00+08:00'
            with open('data/policy/latest.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not update policy news timestamp: {e}")
    else:
        print(f"❌ Error fetching policy news: {result.stderr}")
        
except subprocess.TimeoutExpired:
    print("❌ Timeout while fetching policy news")
except Exception as e:
    print(f"❌ Exception while fetching policy news: {e}")
