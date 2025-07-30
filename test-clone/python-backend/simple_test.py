import asyncio
import websockets
import json

async def test():
    try:
        async with websockets.connect("ws://localhost:8766") as ws:
            print("Connected!")
            await ws.send(json.dumps({"type": "text", "text": "test"}))
            response = await ws.recv()
            print("Response:", response)
    except Exception as e:
        print("Error:", e)

asyncio.run(test())