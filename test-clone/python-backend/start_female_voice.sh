#!/bin/bash

echo "🚀 Starting Female Voice Server..."

# Kill existing server
lsof -ti :8765 | xargs kill -9 2>/dev/null

# Set API key
export GOOGLE_API_KEY="AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

# Start female voice server
cd "$(dirname "$0")"
source venv/bin/activate
python3 female_voice_server.py