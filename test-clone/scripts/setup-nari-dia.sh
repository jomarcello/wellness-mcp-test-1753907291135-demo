#!/bin/bash

# Nari Dia TTS Setup Script voor VAPI Demo
# Dit script installeert en configureert Nari Dia TTS voor gebruik in de VAPI voice demo

set -e

echo "🎙️ Setting up Nari Dia TTS for VAPI Demo..."
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.9+ and try again."
    exit 1
fi

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is required but not installed."
    echo "Please install Git and try again."
    exit 1
fi

# Create nari-dia directory if it doesn't exist
if [ ! -d "nari-dia" ]; then
    echo "📥 Cloning Nari Dia TTS repository..."
    git clone https://github.com/pinokiofactory/Nari-Dia-TTS.git nari-dia
    cd nari-dia
else
    echo "📁 Nari Dia directory already exists, updating..."
    cd nari-dia
    git pull origin main
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing required packages..."
pip install --upgrade pip

# Install PyTorch (CPU version for compatibility)
echo "🔥 Installing PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install other requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "📋 Installing common TTS dependencies..."
    pip install gradio transformers scipy numpy soundfile librosa
fi

# Install additional dependencies that might be missing
pip install huggingface_hub transformers accelerate

echo "✅ Installation completed!"
echo ""
echo "🚀 To start Nari Dia TTS server:"
echo "   1. cd nari-dia"
echo "   2. source venv/bin/activate"
echo "   3. python app.py --device cpu"
echo ""
echo "🌐 The server will be available at: http://localhost:7860"
echo "🔗 API endpoint: http://localhost:7860/api/v1/generate"
echo ""
echo "📱 To use in VAPI demo:"
echo "   1. Make sure Nari Dia server is running"
echo "   2. Open your VAPI demo at http://localhost:3000"
echo "   3. Select 'Nari Dia TTS' in the voice selector"
echo "   4. Start a conversation in Dutch!"
echo ""
echo "💡 Tip: Use GPU for better performance:"
echo "   python app.py --device cuda (requires CUDA setup)" 