#!/usr/bin/env python3
"""
Conversational Voice Agent with Female Voice
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

# Configuration with female voice preference
MODEL = "models/gemini-2.0-flash-live-001"
CONFIG = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "You are Robin, a friendly female assistant for BeautyMed Clinic. Respond in Thai with a warm, caring, and professional tone. You are helpful, knowledgeable about beauty treatments, and always speak in a gentle, feminine way.",
    "generation_config": {
        "response_mime_type": "audio/pcm",
        "speech_config": {
            "voice_config": {
                "prebuilt_voice_config": {
                    "voice_name": "Aoede"  # Try female voice
                }
            }
        }
    }
}

# Alternative config to try
CONFIG_ALT = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "คุณคือ Robin ผู้ช่วยสาวสวยของ BeautyMed Clinic พูดเสียงหวานนุ่มนวล เป็นมิตร และเต็มไปด้วยความอบอุ่น ตอบคำถามเกี่ยวกับความงามด้วยความเชี่ยวชาญ"
}

async def handle_connection(websocket):
    """Handle WebSocket connection with female voice"""
    logger.info("👩 Frontend connected - Female Voice Mode")
    
    try:
        client = genai.Client()
        
        # Try with voice config first, fallback to basic
        try:
            session_config = CONFIG
            async with client.aio.live.connect(model=MODEL, config=session_config) as session:
                logger.info("✅ Connected with voice config")
                await run_conversation(session, websocket)
        except Exception as e:
            logger.warning(f"Voice config failed: {e}, trying basic config")
            session_config = CONFIG_ALT
            async with client.aio.live.connect(model=MODEL, config=session_config) as session:
                logger.info("✅ Connected with basic config")
                await run_conversation(session, websocket)
            
    except Exception as e:
        logger.error(f"❌ Connection error: {e}")
        import traceback
        traceback.print_exc()

async def run_conversation(session, websocket):
    """Run the conversation loop"""
    # Send initial greeting
    await session.send(input="สวัสดีค่ะ ดิฉันโรบินครับ ยินดีต้อนรับสู่ BeautyMed Clinic มีอะไรให้ช่วยเหลือไหมคะ", end_of_turn=True)
    
    # Handle messages concurrently
    async def handle_frontend():
        async for message in websocket:
            data = json.loads(message)
            logger.info(f"📥 Frontend: {data.get('type', 'unknown')}")
            
            if data.get("type") == "text":
                logger.info(f"📝 Text: {data['text']}")
                await session.send(input=data["text"], end_of_turn=True)
                
            elif data.get("type") == "audio_continuous":
                logger.info(f"🎤 Audio: {len(data.get('data', ''))} chars")
                try:
                    audio_data = base64.b64decode(data["data"])
                    await session.send_realtime_input(audio={"data": audio_data, "mime_type": "audio/pcm"})
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
                logger.info(f"💬 Text: {response.text}")
                await websocket.send(json.dumps({
                    "type": "text",
                    "text": response.text
                }))
                
    # Run both tasks
    await asyncio.gather(handle_frontend(), handle_gemini())

async def main():
    """Start female voice server"""
    logger.info("🚀 Starting Female Voice Server")
    
    async with websockets.serve(handle_connection, "localhost", 8765):
        logger.info("✅ Female voice server started on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())