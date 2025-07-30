# 🎤 Quick Start Guide - Conversational Voice Agent

## ✅ **Fixed Issues**
- ✅ Updated to `gemini-2.5-flash-preview-native-audio-dialog` (official conversational model)
- ✅ Implemented real-time streaming with proper async pattern
- ✅ Fixed audio buffer management (1024 chunks, 16kHz input, 24kHz output)
- ✅ Eliminated choppy audio with concurrent audio processing
- ✅ Created proper virtual environment setup

## 🚀 **Start the Application**

### Terminal 1: Backend
```bash
cd python-backend
./start_server.sh
```

### Terminal 2: Frontend
```bash
npm run dev
```

### Terminal 3: Open Browser
```
http://localhost:3000
```

## 📋 **Usage**
1. Click "เริ่มการสนทนาแบบ Real-time" 
2. Allow microphone access
3. Start talking - Robin will respond in real-time
4. Audio plays directly from speakers
5. Use headphones to prevent echo

## 🔧 **Troubleshooting**

### Backend Issues
```bash
# Check if backend is running
lsof -i :8765

# Test audio setup
cd python-backend
source venv/bin/activate
python test_audio.py

# View backend logs
tail -f logs/server.log
```

### Frontend Issues
```bash
# Check console for WebSocket errors
# F12 → Console → Look for WebSocket messages
```

## 🎯 **Success Indicators**
- Backend shows: "Conversational voice agent started on ws://localhost:8765"
- Frontend shows: "เชื่อมต่อแล้ว" (Connected)
- Audio status shows: "กำลังฟังและพูดแบบ Real-time"
- No WebSocket 1006 errors

## 📱 **Features**
- **Real-time conversation** - No button pressing needed
- **Thai language support** - Robin responds in Thai
- **Direct audio streaming** - Audio plays from backend to speakers
- **Smooth audio** - No choppy audio with official buffer sizes
- **Text backup** - Can also type messages for testing