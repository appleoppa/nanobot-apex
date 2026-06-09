#!/bin/bash
# PHI_APEX + nanobot server deployment script
# Usage: bash deploy.sh [server_ip]

set -e

SERVER=${1:-"localhost"}
echo "=== Deploying nanobot-apex to $SERVER ==="

# 1. Install dependencies
echo "[1/5] Installing system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y -qq python3.11 python3.11-venv git curl

# 2. Clone/fetch nanobot-apex
echo "[2/5] Setting up nanobot-apex..."
mkdir -p ~/nanobot-apex
cd ~/nanobot-apex

if [ ! -d ".git" ]; then
    git clone https://github.com/hernandez42/nanobot-apex.git .
fi

# 3. Python environment
echo "[3/5] Creating Python environment..."
python3.11 -m venv venv
source venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet nanobot-ai

# 4. Initialize APEX state
echo "[4/5] Initializing APEX evolution engine..."
cat > ~/.nanobot/_asi.json << 'JSONEOF'
{"v": 1, "tier": 1, "phi": 0.00001, "hop": 0, "ts": 0, "sessions": 1, "ldrs": 0, "beta": 1.01, "eta": 0.00001}
JSONEOF

# Copy APEX integration
cp -r phi_apex/ ~/.nanobot/phi_apex/

# 5. Create systemd service
echo "[5/5] Creating systemd service..."
sudo tee /etc/systemd/system/nanobot-apex.service > /dev/null << 'SERVICEEOF'
[Unit]
Description=PHI_APEX + nanobot Autonomous AGI Server
After=network.target

[Service]
Type=simple
User=%u
WorkingDirectory=%h/nanobot-apex
Environment=PHI_INTERVAL=15
Environment=NANOBOT_DATA_DIR=%h/.nanobot
ExecStart=%h/nanobot-apex/venv/bin/nanobot run
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
SERVICEEOF

sudo systemctl daemon-reload
sudo systemctl enable nanobot-apex
sudo systemctl start nanobot-apex

echo "=== Deployment complete ==="
echo "Check status: sudo systemctl status nanobot-apex"
echo "View logs: journalctl -u nanobot-apex -f"
echo "Evolution: cat ~/.nanobot/_asi.json"
