# 🛠️ Troubleshooting Guide

## ✅ **Backend Server Status**
De backend server draait nu succesvol op `ws://localhost:8765`

## 🚀 **Stappen om te Starten**

### 1. Start Backend Server
```bash
# Optie 1: Simpel
cd python-backend
python3 run_server.py

# Optie 2: Met virtual environment
cd python-backend
source venv/bin/activate
python3 working_server.py
```

### 2. Controleer of Server Draait
```bash
# Check of port 8765 in gebruik is
lsof -i :8765

# Zou moeten tonen:
# COMMAND   PID           USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
# Python  xxxxx jovannitilborg    8u  IPv4 ...  TCP localhost:ultraseek-http (LISTEN)
```

### 3. Start Frontend
```bash
# In een nieuwe terminal
npm run dev
```

### 4. Open Browser
```
http://localhost:3000
```

## 🔧 **Als WebSocket 1006 Error Blijft**

### Stap 1: Kill Alle Python Processen
```bash
pkill -f working_server
pkill -f python3
```

### Stap 2: Start Backend Opnieuw
```bash
cd python-backend
source venv/bin/activate
python3 working_server.py
```

### Stap 3: Controleer Logs
De backend zou moeten tonen:
```
INFO:__main__:Starting Conversational Voice Agent
INFO:__main__:Server will run on ws://localhost:8765
INFO:websockets.server:server listening on 127.0.0.1:8765
INFO:__main__:Conversational voice agent started on ws://localhost:8765
```

## 📱 **Browser Console Check**
1. Open F12 Developer Tools
2. Ga naar Console tab
3. Probeer verbinding te maken
4. Kijk of je deze berichten ziet:
   - "Connected to Conversational Gemini Live API" ✅
   - "WebSocket connection failed" ❌

## 🎯 **Success Checklist**
- [ ] Backend toont "server listening on 127.0.0.1:8765"
- [ ] `lsof -i :8765` toont Python proces
- [ ] Frontend toont "เชื่อมต่อแล้ว" (Connected)
- [ ] Geen WebSocket 1006 errors in console
- [ ] Audio status toont "กำลังฟังและพูดแบบ Real-time"

## 🚨 **Meest Voorkomende Problemen**

### 1. "Module not found" Error
```bash
cd python-backend
source venv/bin/activate
pip install -r requirements.txt
```

### 2. "Permission denied" Error
```bash
chmod +x run_server.py
chmod +x start_server.sh
```

### 3. "Port already in use" Error
```bash
lsof -ti :8765 | xargs kill -9
```

## 💡 **Als Niets Werkt**
```bash
# Complete reset
cd python-backend
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 working_server.py
```