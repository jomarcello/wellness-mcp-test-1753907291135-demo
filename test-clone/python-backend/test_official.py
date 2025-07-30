#!/usr/bin/env python3
"""
Test the official voice agent
"""
import asyncio
import websockets
import json

async def test_official_server():
    """Test the official server implementation"""
    try:
        async with websockets.connect('ws://localhost:8765') as websocket:
            print("✅ Connected to official server!")
            
            # Send text message
            await websocket.send(json.dumps({
                "type": "text",
                "text": "สวัสดี Robin"
            }))
            print("📤 Text message sent")
            
            # Listen for responses
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                print(f"📥 Response: {data}")
                
                if data.get('type') == 'text':
                    print("✅ Text response received!")
                elif data.get('type') == 'audio':
                    print("✅ Audio response received!")
                    
            except asyncio.TimeoutError:
                print("⏰ No response within 5 seconds")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_official_server())