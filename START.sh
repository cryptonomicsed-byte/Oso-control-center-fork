#!/bin/bash

# OSO Control Center Startup Script
# Starts API server and optionally opens dashboard

echo "🔥 Starting Ọ̀ṢỌ́VM v7 — ÀṣẹVault Control Center"

cd "$(dirname "$0")"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install it first."
    exit 1
fi

# Install dependencies if needed
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv backend/venv
    source backend/venv/bin/activate
    pip install -q -r backend/requirements.txt
else
    source backend/venv/bin/activate
fi

# Start API server
echo "🚀 Starting API server on http://127.0.0.1:8888"
cd backend
python app.py &
API_PID=$!

sleep 2

# Check if server started
if ! curl -s http://127.0.0.1:8888 > /dev/null; then
    echo "❌ API server failed to start"
    exit 1
fi

echo "✓ API server running (PID: $API_PID)"

# Optionally open dashboard
if command -v xdg-open &> /dev/null; then
    echo "🌐 Opening dashboard..."
    xdg-open "file://$(pwd)/../dashboard/index.html" &
elif command -v open &> /dev/null; then
    open "file://$(pwd)/../dashboard/index.html" &
fi

echo ""
echo "📊 Dashboard: file://$(pwd)/../dashboard/index.html"
echo "📡 API: http://127.0.0.1:8888/api/v1"
echo ""
echo "Press Ctrl+C to stop"
wait $API_PID
