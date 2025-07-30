#!/usr/bin/env python3
"""
Debug version to find the 1011 error
"""
import asyncio
import os
import json
import logging
import websockets
from google import genai

# Configure detailed logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# API Configuration
os.environ["GOOGLE_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

# Test with simplest possible configuration
MODEL = "gemini-2.5-flash-preview-native-audio-dialog"
CONFIG = {"response_modalities": ["TEXT"]}  # Start with text only

client = genai.Client()

async def handle_connection(websocket, path):
    """Debug connection handler"""
    logger.info("=== Frontend connected ===")
    
    try:
        logger.info(f"Attempting to connect to model: {MODEL}")
        logger.info(f"With config: {CONFIG}")
        
        async with client.aio.live.connect(model=MODEL, config=CONFIG) as session:
            logger.info("✅ Successfully connected to Gemini Live API")
            
            # Send initial message
            await session.send(input="Hello, can you hear me?", end_of_turn=True)
            logger.info("✅ Initial message sent")
            
            # Listen for frontend messages
            async for message in websocket:
                logger.info(f"Received frontend message: {message}")
                
                data = json.loads(message)
                if data.get("type") == "text":
                    logger.info(f"Sending text to Gemini: {data['text']}")
                    await session.send(input=data["text"], end_of_turn=True)
                    
                    # Get response
                    turn = session.receive()
                    async for response in turn:
                        if response.text:
                            logger.info(f"Gemini response: {response.text}")
                            await websocket.send(json.dumps({
                                "type": "text",
                                "text": response.text
                            }))
                            break
                            
    except Exception as e:
        logger.error(f"❌ Connection error: {e}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        
        try:
            await websocket.send(json.dumps({
                "type": "error",
                "message": str(e)
            }))
        except:
            pass

async def main():
    """Start debug server"""
    logger.info("Starting debug server...")
    
    async with websockets.serve(handle_connection, "localhost", 8765):
        logger.info("Debug server started on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())