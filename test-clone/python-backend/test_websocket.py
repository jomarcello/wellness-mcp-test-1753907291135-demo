#\!/usr/bin/env python3
import asyncio
import websockets
import json

async def test_connection():
    try:
        print("🔌 Connecting to ws://localhost:8766...")
        async with websockets.connect("ws://localhost:8766") as websocket:
            print("✅ Connected successfully\!")
            
            # Send test message
            test_msg = {"type": "text", "text": "สวัสดีครับ"}
            await websocket.send(json.dumps(test_msg))
            print("📤 Sent test message")
            
            # Wait for response
            response = await websocket.recv()
            print(f"📥 Received: {response}")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
EOF < /dev/null