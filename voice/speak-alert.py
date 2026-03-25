#!/usr/bin/env python3
# voice/speak-alert.py — Convert alert text to speech via ElevenLabs

import os
import requests
import subprocess
from datetime import datetime

# Your ElevenLabs API key (cached from yesterday)
ELEVENLABS_API_KEY = "sk_..."  # Already authenticated
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

ALERT_TEXT = "USD slash CNY just breached seven point three five"
OUTPUT_FILE = '../alerts/last-alert.mp3'

# Generate speech
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": ELEVENLABS_API_KEY
}
payload = {
    "text": ALERT_TEXT,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 200:
    with open(OUTPUT_FILE, 'wb') as f:
        f.write(response.content)
    print(f'✅ Voice alert saved: {OUTPUT_FILE}')
    
    # Play it
    try:
        subprocess.run(['mpg123', OUTPUT_FILE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print('🔊 Alert played')
    except FileNotFoundError:
        print('⚠️  mpg123 not found — play manually')
else:
    print(f'❌ ElevenLabs error: {response.status_code} {response.text[:100]}')
