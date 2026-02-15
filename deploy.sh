#!/bin/bash
set -e

echo "=== Deploying Web Grab & Capture ==="

# Configuration
LOCAL_PATH="/home/lucas/Documents/Web-Grab-Capture"
SERVER_PATH="/var/www/webgrab"
VENV_PATH="$SERVER_PATH/.venv"

# Sync application files
echo "Syncing application files..."
sudo mkdir -p "$SERVER_PATH"
sudo rsync -av \
    --exclude '.venv' \
    --exclude '.git' \
    --exclude '__pycache__' \
    --exclude 'exports' \
    --exclude '*.pyc' \
    "$LOCAL_PATH/" "$SERVER_PATH/"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    sudo python3 -m venv "$VENV_PATH"
fi

# Install dependencies
echo "Installing dependencies..."
sudo "$VENV_PATH/bin/pip" install -r "$SERVER_PATH/requirements.txt" --quiet

# Set permissions
echo "Setting permissions..."
sudo chown -R www-data:www-data "$SERVER_PATH"
sudo chmod -R 755 "$SERVER_PATH"

# Create exports directory (writable for image downloads)
sudo mkdir -p "$SERVER_PATH/exports"
sudo chown www-data:www-data "$SERVER_PATH/exports"

# Setup PM2 processes for Streamlit UI and FastAPI API
echo "Setting up PM2 processes..."

# Stop existing processes if running
sudo pm2 delete webgrab-ui 2>/dev/null || true
sudo pm2 delete webgrab-api 2>/dev/null || true

# Start Streamlit UI (port 8501)
sudo pm2 start "$VENV_PATH/bin/python" \
    --name webgrab-ui \
    --interpreter none \
    -- -m streamlit run "$SERVER_PATH/app.py" \
    --server.port 8501 \
    --server.headless true \
    --server.baseUrlPath webgrab \
    --server.enableXsrfProtection false \
    --browser.gatherUsageStats false

# Start FastAPI API (port 8000)
sudo pm2 start "$VENV_PATH/bin/python" \
    --name webgrab-api \
    --interpreter none \
    --cwd "$SERVER_PATH" \
    -- -m uvicorn api:app \
    --host 0.0.0.0 \
    --port 8000 \
    --root-path /webgrab-api

# Save PM2 process list
sudo pm2 save

echo ""
echo "=== Deployment Complete! ==="
echo "Streamlit UI:  https://lucascode.org/webgrab/"
echo "FastAPI Docs:  https://lucascode.org/webgrab-api/docs"
echo ""
echo "Next step: Add the Nginx location blocks (see nginx-webgrab.conf)"
