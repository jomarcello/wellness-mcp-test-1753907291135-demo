#!/bin/bash

# Start the conversational voice agent backend
cd "$(dirname "$0")"

echo "🚀 Starting Conversational Voice Agent Backend..."
echo "📍 Location: $(pwd)"

# Activate virtual environment
source venv/bin/activate

# Start the server
echo "🎯 Starting server on ws://localhost:8765..."
python working_server.py