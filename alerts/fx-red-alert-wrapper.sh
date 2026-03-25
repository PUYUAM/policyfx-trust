#!/bin/bash

# FX Red Alert Wrapper - Sets env vars and runs the Python script

# Load environment variables from a secure location or set them here
# For security, these should be set in the cron environment or loaded from a config file

# Set Telegram credentials (replace with your actual values)
export TELEGRAM_TOKEN="${TELEGRAM_TOKEN:-YOUR_TELEGRAM_TOKEN_HERE}"
export TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-YOUR_TELEGRAM_CHAT_ID_HERE}"

# Run the Python script
python3 alerts/fx-red-alert-telegram.py
