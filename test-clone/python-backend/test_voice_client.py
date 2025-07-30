#!/usr/bin/env python3
"""
Test client voor voice agent logging
"""
import asyncio
import websockets
import json

async def test_client():
    uri = "ws://localhost:8766"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to voice agent")
            print("📝 Sending test message...")
            
            # Send a test text message
            await websocket.send(json.dumps({
                "type": "text",
                "text": "สวัสดีครับ"
            }))
            
            print("⏳ Waiting for response...")
            await asyncio.sleep(5)
            
            print("🛑 Stopping connection...")
            await websocket.send(json.dumps({
                "type": "stop"
            }))
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_client())