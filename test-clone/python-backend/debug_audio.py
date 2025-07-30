#!/usr/bin/env python3
"""
Debug audio input to see if frontend is sending audio
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

# API Configuration
os.environ["GOOGLE_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

# Configuration with voice preference
MODEL = "models/gemini-2.0-flash-live-001"
CONFIG = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "คุณคือ Robin ผู้ช่วยสาวน่ารักของ BeautyMed Clinic คลินิกความงาม ตอบเป็นภาษาไทยด้วยเสียงหวานๆ เป็นมิตร",
    "speech_config": {
        "voice_config": {
            "prebuilt_voice_config": {
                "voice_name": "Charon"  # Female voice
            }
        }
    }
}

async def handle_connection(websocket):
    """Debug connection handler"""
    logger.info("=== Frontend connected ===")
    
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
                    logger.info(f"📥 Frontend message: {data.get('type', 'unknown')}")
                    
                    if data.get("type") == "text":
                        logger.info(f"📝 Text: {data['text']}")
                        await session.send(input=data["text"], end_of_turn=True)
                        
                    elif data.get("type") == "audio_continuous":
                        logger.info(f"🎤 Audio chunk: {len(data.get('data', ''))} bytes")
                        try:
                            audio_data = base64.b64decode(data["data"])
                            logger.info(f"🎤 Decoded audio: {len(audio_data)} bytes")
                            await session.send_realtime_input(audio={"data": audio_data, "mime_type": "audio/pcm"})
                            logger.info("✅ Audio sent to Gemini")
                        except Exception as e:
                            logger.error(f"❌ Audio error: {e}")
                        
            async def handle_gemini():
                async for response in session.receive():
                    if response.data is not None:
                        logger.info(f"🔊 Audio response: {len(response.data)} bytes")
                        await websocket.send(json.dumps({
                            "type": "audio",
                            "data": base64.b64encode(response.data).decode()
                        }))
                        
                    if response.text is not None:
                        logger.info(f"💬 Text response: {response.text}")
                        await websocket.send(json.dumps({
                            "type": "text",
                            "text": response.text
                        }))
                        
            # Run both tasks
            await asyncio.gather(handle_frontend(), handle_gemini())
            
    except Exception as e:
        logger.error(f"❌ Connection error: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Start debug server"""
    logger.info("🚀 Starting Debug Audio Server")
    
    async with websockets.serve(handle_connection, "localhost", 8765):
        logger.info("✅ Debug server started on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())