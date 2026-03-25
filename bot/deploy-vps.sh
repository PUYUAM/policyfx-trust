#!/bin/bash
# bot/deploy-vps.sh — Deploy Policy+FX Telegram Bot to VPS

set -e

echo "🚀 Deploying Policy+FX Telegram Bot to VPS..."

echo "🔧 Step 1: Installing Python & pip"
sudo apt-get update
sudo apt-get install -y python3 python3-pip curl

echo "📦 Step 2: Installing dependencies"
pip3 install --user -r /home/puyuam/.openclaw/workspace/bot/requirements.txt

echo "📁 Step 3: Creating systemd service"
sudo tee /etc/systemd/system/policyfx-telegram-bot.service > /dev/null << 'EOF'
[Unit]
Description=Policy+FX Telegram Bot
After=network.target

[Service]
Type=simple
User=puyuam
WorkingDirectory=/home/puyuam/.openclaw/workspace/bot
ExecStart=/usr/bin/python3 /home/puyuam/.openclaw/workspace/bot/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=policyfx-telegram-bot

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable policyfx-telegram-bot.service

# Start service
echo "▶️ Step 4: Starting service"
sudo systemctl start policyfx-telegram-bot.service

# Verify
echo "✅ Deployment complete. Status:"
sudo systemctl status policyfx-telegram-bot.service --no-pager | head -10

echo "📝 Logs: journalctl -u policyfx-telegram-bot.service -f"
