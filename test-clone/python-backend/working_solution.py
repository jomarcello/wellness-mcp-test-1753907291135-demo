#!/usr/bin/env python3
"""
Working Solution - Based on exact cookbook pattern
"""
import asyncio
import os
import json
import logging
import websockets
import base64
from google import genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

# Test with working model first
MODEL = "models/gemini-2.0-flash-live-001"
CONFIG = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic คลินิกความงาม ตอบเป็นภาษาไทยเท่านั้น"
}

async def handle_connection(websocket):
    """Handle WebSocket connection"""
    logger.info("Frontend connected")
    
    try:
        client = genai.Client()
        
        async with client.aio.live.connect(model=MODEL, config=CONFIG) as session:
            logger.info("✅ Connected to Gemini Live API")
            
            # Send initial greeting
            await session.send(input="สวัสดีค่ะ ยินดีต้อนรับสู่ BeautyMed Clinic", end_of_turn=True)
            
            # Handle messages concurrently
            async def handle_frontend():
                async for message in websocket:
                    data = json.loads(message)
                    if data.get("type") == "text":
                        await session.send(input=data["text"], end_of_turn=True)
                    elif data.get("type") == "audio_continuous":
                        # Handle continuous audio from frontend
                        try:
                            audio_data = base64.b64decode(data["data"])
                            await session.send_realtime_input(audio={"data": audio_data, "mime_type": "audio/pcm"})
                        except Exception as e:
                            logger.error(f"Error processing frontend audio: {e}")
                        
            async def handle_gemini():
                async for response in session.receive():
                    if response.data is not None:
                        await websocket.send(json.dumps({
                            "type": "audio",
                            "data": base64.b64encode(response.data).decode()
                        }))
                    if response.text is not None:
                        logger.info(f"Text: {response.text}")
                        await websocket.send(json.dumps({
                            "type": "text",
                            "text": response.text
                        }))
                        
            # Run both tasks
            await asyncio.gather(handle_frontend(), handle_gemini())
            
    except Exception as e:
        logger.error(f"Connection error: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            await websocket.send(json.dumps({
                "type": "error",
                "message": str(e)
            }))
        except:
            pass
    finally:
        logger.info("Frontend disconnected")

async def main():
    """Start the working solution"""
    logger.info("Starting Working Solution")
    
    async with websockets.serve(handle_connection, "localhost", 8765):
        logger.info("✅ Working solution started on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())