#!/usr/bin/env python3
"""
Real Conversational Voice Agent - Turn-based
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

# Configuration for conversational mode - Native Audio Dialog
MODEL = "models/gemini-2.5-flash-preview-native-audio-dialog"
CONFIG = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "You are Robin, a warm and friendly female assistant for BeautyMed Clinic in Thailand. Always respond in Thai with a caring, professional tone. Keep responses concise (2-3 sentences). You help with beauty treatments, appointments, and general clinic information.",
    "speech_config": {
        "voice_config": {
            "prebuilt_voice_config": {
                "voice_name": "Aoede"
            }
        }
    }
}

class ConversationalAgent:
    def __init__(self):
        self.is_listening = True
        self.is_speaking = False
        
    async def handle_connection(self, websocket):
        """Handle conversational connection"""
        logger.info("👋 Client connected for conversation")
        
        try:
            client = genai.Client()
            
            async with client.aio.live.connect(model=MODEL, config=CONFIG) as session:
                logger.info("✅ Connected to Gemini")
                
                # Send initial greeting
                await session.send(input="สวัสดีค่ะ ดิฉันโรบินค่ะ ยินดีต้อนรับสู่ BeautyMed Clinic มีอะไรให้ช่วยเหลือไหมคะ", end_of_turn=True)
                logger.info("🗣️ Robin: Initial greeting sent")
                
                # Handle conversation
                await asyncio.gather(
                    self.handle_frontend(websocket, session),
                    self.handle_gemini(websocket, session)
                )
                
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            import traceback
            traceback.print_exc()

    async def handle_frontend(self, websocket, session):
        """Handle frontend messages"""
        try:
            async for message in websocket:
                data = json.loads(message)
                
                if data.get("type") == "text":
                    logger.info(f"💬 User text: {data['text']}")
                    self.is_listening = False
                    await session.send(input=data["text"], end_of_turn=True)
                    
                elif data.get("type") == "audio_continuous" and self.is_listening:
                    try:
                        audio_data = base64.b64decode(data["data"])
                        await session.send_realtime_input(audio={"data": audio_data, "mime_type": "audio/pcm"})
                    except Exception as e:
                        logger.error(f"❌ Audio error: {e}")
                        
                elif data.get("type") == "start_listening":
                    self.is_listening = True
                    logger.info("👂 Listening mode ON")
                    
                elif data.get("type") == "stop_listening":
                    self.is_listening = False
                    logger.info("🔇 Listening mode OFF")
                    
        except Exception as e:
            logger.error(f"❌ Frontend error: {e}")

    async def handle_gemini(self, websocket, session):
        """Handle Gemini responses"""
        try:
            async for response in session.receive():
                if response.data is not None:
                    # Robin is speaking - stop listening
                    self.is_speaking = True
                    self.is_listening = False
                    
                    logger.info(f"🗣️ Robin speaking: {len(response.data)} bytes")
                    await websocket.send(json.dumps({
                        "type": "audio",
                        "data": base64.b64encode(response.data).decode()
                    }))
                    
                if response.text is not None:
                    logger.info(f"💭 Robin text: {response.text}")
                    await websocket.send(json.dumps({
                        "type": "text", 
                        "text": response.text
                    }))
                    
                # Check if turn is complete
                if hasattr(response, 'turn_complete') and response.turn_complete:
                    # Robin finished speaking - resume listening
                    self.is_speaking = False
                    self.is_listening = True
                    logger.info("✅ Turn complete - resuming listening")
                    
                    await websocket.send(json.dumps({
                        "type": "turn_complete"
                    }))
                    
        except Exception as e:
            logger.error(f"❌ Gemini error: {e}")

async def main():
    """Start conversational server"""
    agent = ConversationalAgent()
    
    logger.info("🚀 Starting Real Conversational Agent")
    
    async with websockets.serve(agent.handle_connection, "localhost", 8765):
        logger.info("✅ Conversational agent ready on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())