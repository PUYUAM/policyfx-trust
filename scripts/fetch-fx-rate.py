#!/usr/bin/env python3
# scripts/fetch-fx-rate.py — Fetch USD/CNY rate using lib/fetcher.py

import subprocess
import sys
import os

# Ensure the data directory exists
os.makedirs('data/fx', exist_ok=True)

# Use the fetcher library to get USD/CNY rate
# We'll use exchangerate-api.com which provides USD/CNY directly
try:
    result = subprocess.run([
        'python3', 
        'lib/fetcher.py', 
        '--url', 'https://api.exchangerate-api.com/v4/latest/USD', 
        '--cache-ttl', '1800', 
        '--output', 'data/fx/latest.json'
    ], capture_output=True, text=True, timeout=30)
    
    if result.returncode == 0:
        print(f"✅ Successfully fetched FX rate: {result.stdout[:200]}...")
        # Extract and display the rate
        if '"USD"' in result.stdout:
            # Parse the JSON to get USD/CNY rate
            import json
            try:
                data = json.loads(result.stdout)
                if 'rates' in data and 'CNY' in data['rates']:
                    rate = data['rates']['CNY']
                    print(f"📈 USD/CNY rate: {rate:.3f}")
                else:
                    print("⚠️  CNY rate not found in response")
            except json.JSONDecodeError:
                print("⚠️  Could not parse JSON response")
    else:
        print(f"❌ Error fetching FX rate: {result.stderr}")
        
except subprocess.TimeoutExpired:
    print("❌ Timeout while fetching FX rate")
except Exception as e:
    print(f"❌ Exception while fetching FX rate: {e}")
