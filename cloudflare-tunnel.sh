#!/bin/bash
# cloudflare-tunnel.sh — Expose ui/ dashboard securely via Cloudflare Tunnel

set -e

echo "🔐 Setting up Cloudflare Tunnel for Policy+FX Dashboard..."

# Install cloudflared if missing
if ! command -v cloudflared &> /dev/null; then
  echo "📦 Installing cloudflared..."
  if [[ "$(uname)" == "Linux" ]]; then
    curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared
    chmod +x /usr/local/bin/cloudflared
  else
    echo "⚠️  Please install cloudflared manually for your OS: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
    exit 1
  fi
fi

# Start simple HTTP server for ui/
cd /home/puyuam/.openclaw/workspace && python3 -m http.server 8000 --directory ui/ > /dev/null 2>&1 &
SERVER_PID=$!
sleep 2

echo "🚀 Starting Cloudflare Tunnel..."
echo "💡 This will open a browser window for Cloudflare auth."

echo "   Press Ctrl+C to cancel, then run 'kill $SERVER_PID' to stop the server."

cloudflared tunnel --url http://localhost:8000 --name policyfx-dashboard

# Cleanup on exit
trap "kill $SERVER_PID 2>/dev/null" EXIT
