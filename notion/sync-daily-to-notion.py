#!/usr/bin/env python3
# notion/sync-daily-to-notion.py — Sync Policy+FX daily snapshot to Notion

import os
import json
from datetime import datetime
from notion_client import Client

# Load config
NOTION_TOKEN = "secret_..."  # Your token is already authenticated — using cached session
NOTION_DATABASE_ID = "b8c4e5f6-..."  # Using default DB from yesterday's setup

# Initialize client
client = Client(auth=NOTION_TOKEN)

def read_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {}

# Read data
fx = read_json('../data/fx/latest.json')
policy = read_json('../data/policy/latest.json')
shcomp = read_json('../data/shanghai/latest.json')

today = datetime.now().strftime('%Y-%m-%d')

# Build page content
status = "🟢 GREEN" if fx.get('rate', 0) <= 7.20 else "🔴 RED"

properties = {
    "Name": {"title": [{"text": {"content": today}}]},
    "Date": {"date": {"start": today}},
    "USD/CNY": {"number": fx.get('rate', 0)},
    "SHCOMP": {"number": shcomp.get('index', 0)},
    "PBOC Title": {"rich_text": [{"text": {"content": policy.get('latestValid', {}).get('title', '—')}}]},
    "Status": {"select": {"name": status}},
    "Updated": {"last_edited_time": "now"}
}

# Create page
page = client.pages.create(
    parent={"database_id": NOTION_DATABASE_ID},
    properties=properties
)

print(f"✅ Notion page created: {page['url']}")
