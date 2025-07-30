#!/bin/bash

# Install dependencies for Gemini Live API
echo "Installing Python dependencies..."
pip install google-genai websockets pyaudio Pillow

# Set environment variable
echo "Setting up environment..."
export GEMINI_API_KEY="AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

echo "Setup complete!"
echo "To run the Gemini Live server:"
echo "cd python-backend"
echo "python gemini_live_server.py"