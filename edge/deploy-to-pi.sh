#!/bin/bash
# edge/deploy-to-pi.sh — Deploy Policy+FX dashboard as Raspberry Pi kiosk

set -e

echo "🖥️  Setting up Policy+FX Dashboard on Raspberry Pi..."

# Install Chromium kiosk deps
sudo apt-get update
sudo apt-get install -y chromium-browser x11-xserver-utils lightdm

# Configure autologin
sudo systemctl set-default graphical.target
sudo mkdir -p /etc/lightdm/lightdm.conf.d
sudo tee /etc/lightdm/lightdm.conf.d/01-autologin.conf > /dev/null << 'EOF'
[Seat:*]
autologin-user=pi
autologin-user-timeout=0
user-session=lxde
EOF

# Create kiosk script
sudo tee /usr/local/bin/kiosk.sh > /dev/null << 'EOF'
#!/bin/bash
xset s off
xset -dpms
xset s noblank

# Start Chromium in kiosk mode
/usr/bin/chromium-browser \
  --noerrdialogs \
  --disable-infobars \
  --kiosk \
  --incognito \
  --disable-restore-session-state \
  http://localhost:8000/ui/index.html
EOF
sudo chmod +x /usr/local/bin/kiosk.sh

# Create systemd service
sudo tee /etc/systemd/system/kiosk.service > /dev/null << 'EOF'
[Unit]
Description=Policy+FX Kiosk
Wants=graphical.target
After=graphical.target

[Service]
Type=simple
User=pi
ExecStart=/usr/local/bin/kiosk.sh
Restart=on-abort
RestartSec=10

[Install]
WantedBy=graphical.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable kiosk.service

# Start kiosk
sudo systemctl start kiosk.service

echo "✅ Raspberry Pi kiosk deployed. Reboot to launch."
