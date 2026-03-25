#!/usr/bin/env python3
# lib/fetcher.py — Resilient, auditable, embeddable data fetcher
# Usage: python3 lib/fetcher.py --url https://api.exchangerate-api.com/v4/latest/USD --cache-ttl 1800 --output data/fx/latest.json

import sys
import json
import time
import logging
import csv
import os
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Configure logging
csv_log_path = 'data/audit/log.csv'
os.makedirs(os.path.dirname(csv_log_path), exist_ok=True)
if not os.path.exists(csv_log_path):
    with open(csv_log_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'url', 'status', 'age_seconds', 'error'])

def log_audit(url, status, age_seconds=0, error=''):
    with open(csv_log_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), url, status, age_seconds, error])

def fetch_with_retry(url, max_retries=3, base_delay=1):
    for i in range(max_retries):
        try:
            req = Request(url, headers={'User-Agent': 'OpenClaw-PolicyFX/1.0'})
            with urlopen(req, timeout=10) as response:
                if response.status == 200:
                    log_audit(url, 'success')
                    return response.read().decode('utf-8')
        except (URLError, HTTPError, TimeoutError) as e:
            log_audit(url, 'error', error=str(e))
            if i < max_retries - 1:
                time.sleep(base_delay * (2 ** i))  # exponential backoff
    return None

def load_cache(file_path, max_age_seconds):
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        if 'fetchedAt' in data:
            fetched = datetime.fromisoformat(data['fetchedAt'].replace('Z', '+00:00'))
            if datetime.now(tz=fetched.tzinfo) - fetched < timedelta(seconds=max_age_seconds):
                log_audit(file_path, 'cache_hit', (datetime.now(tz=fetched.tzinfo) - fetched).total_seconds())
                return data
    except Exception as e:
        log_audit(file_path, 'cache_error', error=str(e))
    return None

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--cache-ttl', type=int, default=3600, help='Cache TTL in seconds')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    # Try cache first
    cached = load_cache(args.output, args.cache_ttl)
    if cached:
        print(json.dumps(cached))
        return

    # Fetch fresh
    raw = fetch_with_retry(args.url)
    if raw is None:
        # Cache fallback: serve stale if <24h old
        fallback = load_cache(args.output, 86400)
        if fallback:
            fallback['status'] = 'stale_fallback'
            fallback['ageMinutes'] = round((datetime.now(tz=fallback['fetchedAt'].replace('Z', '+00:00')) - datetime.fromisoformat(fallback['fetchedAt'].replace('Z', '+00:00'))).total_seconds() / 60, 1)
            print(json.dumps(fallback))
            return
        else:
            log_audit(args.url, 'critical_failure')
            raise RuntimeError(f'Failed to fetch {args.url} and no cache available')

    # Parse & enrich
    try:
        data = json.loads(raw)
        data['fetchedAt'] = datetime.now().isoformat() + 'Z'
        data['sourceUrl'] = args.url
        data['ageMinutes'] = 0.0
        data['status'] = 'fresh'
        
        # Write output
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(json.dumps(data))
        
    except json.JSONDecodeError as e:
        log_audit(args.url, 'parse_error', error=str(e))
        raise

if __name__ == '__main__':
    main()
