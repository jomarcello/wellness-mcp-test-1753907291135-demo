#!/usr/bin/env python3
"""
Test the fixed WebSocket server
"""
import asyncio
import websockets
import json

async def test_connection():
    """Test the fixed WebSocket connection"""
    try:
        async with websockets.connect('ws://localhost:8765') as websocket:
            print("✅ WebSocket connection established!")
            
            # Send a test message
            test_message = {
                "type": "text",
                "text": "สวัสดี Robin"
            }
            
            await websocket.send(json.dumps(test_message))
            print("📤 Test message sent:", test_message)
            
            # Wait for response (with timeout)
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                data = json.loads(response)
                print("📥 Response received:", data)
                
                if data.get('type') == 'text':
                    print("✅ Text response working!")
                elif data.get('type') == 'audio':
                    print("✅ Audio response working!")
                    
            except asyncio.TimeoutError:
                print("⏰ No response received within 10 seconds")
                
            print("✅ Connection test completed!")
            
    except websockets.exceptions.ConnectionRefused:
        print("❌ Connection refused - Server not running")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())