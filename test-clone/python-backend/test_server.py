#!/usr/bin/env python3
import asyncio
import websockets
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_client(websocket, path):
    logger.info(f"New client connected: {websocket.remote_address}")
    
    try:
        async for message in websocket:
            data = json.loads(message)
            logger.info(f"Received: {data}")
            
            # Simple echo response
            await websocket.send(json.dumps({
                "type": "response",
                "message": f"Echo: {data}"
            }))
            
    except websockets.exceptions.ConnectionClosed:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error: {e}")
        await websocket.close()

async def main():
    logger.info("Starting test WebSocket server on localhost:8765")
    
    async with websockets.serve(handle_client, "localhost", 8765):
        logger.info("Server is running...")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())