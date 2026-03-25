#!/bin/bash
# secure-edge/airgap-deploy.sh — Deploy fully offline Policy+FX kiosk

set -e

echo "🔒 Deploying air-gapped Policy+FX kiosk..."

# Create offline directory
OFFLINE_DIR="/opt/policyfx-offline"
sudo mkdir -p $OFFLINE_DIR

# Copy static assets
sudo cp -r ../ui/* $OFFLINE_DIR/
sudo cp -r ../data/* $OFFLINE_DIR/data/
sudo cp -r ../lib/* $OFFLINE_DIR/lib/
sudo cp -r ../alerts/* $OFFLINE_DIR/alerts/

# Generate offline dashboard (no remote fetches)
sudo cp ../ui/index.html $OFFLINE_DIR/offline-dashboard.html
sudo sed -i '/<script src="https:\/\/s3\.tradingview\.com\/tv\.js">/d' $OFFLINE_DIR/offline-dashboard.html
sudo sed -i '/new TradingView\.widget(/d' $OFFLINE_DIR/offline-dashboard.html
sudo sed -i '/policyfxAnalytics/d' $OFFLINE_DIR/offline-dashboard.html
sudo sed -i 's|<iframe src="trends/|<img src="trends/|g' $OFFLINE_DIR/offline-dashboard.html

# Configure Chromium for air-gap
sudo tee /usr/local/bin/airgap-kiosk.sh > /dev/null << 'EOF'
#!/bin/bash
xset s off
xset -dpms
xset s noblank

/usr/bin/chromium-browser \
  --noerrdialogs \
  --disable-infobars \
  --kiosk \
  --incognito \
  --disable-features=NetworkService,TranslateUI \
  --disable-restore-session-state \
  --disable-web-security \
  --user-data-dir=/tmp/chrome-airgap \
  file:///opt/policyfx-offline/offline-dashboard.html
EOF
sudo chmod +x /usr/local/bin/airgap-kiosk.sh

# Create systemd service
sudo tee /etc/systemd/system/airgap-kiosk.service > /dev/null << 'EOF'
[Unit]
Description=Air-Gapped Policy+FX Kiosk
Wants=graphical.target
After=graphical.target

[Service]
Type=simple
User=pi
ExecStart=/usr/local/bin/airgap-kiosk.sh
Restart=on-abort
RestartSec=10

[Install]
WantedBy=graphical.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable airgap-kiosk.service

echo "✅ Air-gapped kiosk deployed to $OFFLINE_DIR"
echo "   Launch with: sudo systemctl start airgap-kiosk.service"
