#!/usr/bin/env python3
"""
Google Official Live API Server - Based on Google's Cookbook Example
"""
import asyncio
import os
import json
import logging
import websockets
import base64
from google import genai
from google.genai import types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration
os.environ["GOOGLE_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

# Use Google's official model and config
MODEL = "models/gemini-2.5-flash-preview-native-audio-dialog"

CONFIG = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    media_resolution="MEDIA_RESOLUTION_MEDIUM",
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Aoede")
        )
    ),
    system_instruction="You are Robin, a warm and friendly female assistant for BeautyMed Clinic in Thailand. Always respond in Thai with a caring, professional tone. Keep responses concise (2-3 sentences). You help with beauty treatments, appointments, and general clinic information."
)

# Create client with proper API version
client = genai.Client(
    http_options={"api_version": "v1beta"},
    api_key=os.environ.get("GOOGLE_API_KEY")
)

class GoogleOfficialAgent:
    def __init__(self):
        self.connection_count = 0
        
    async def handle_connection(self, websocket):
        """Handle connection using Google's official approach"""
        self.connection_count += 1
        connection_id = self.connection_count
        logger.info(f"👋 Client #{connection_id} connected - using Google official approach")
        
        try:
            async with client.aio.live.connect(model=MODEL, config=CONFIG) as session:
                logger.info(f"✅ Client #{connection_id} connected to Gemini Live")
                
                # Send initial greeting using new API
                await session.send_client_content(
                    turns=[{"role": "user", "parts": [{"text": "สวัสดีค่ะ ดิฉันโรบินค่ะ ยินดีต้อนรับสู่ BeautyMed Clinic มีอะไรให้ช่วยเหลือไหมคะ"}]}], 
                    turn_complete=True
                )
                logger.info(f"🗣️ Client #{connection_id}: Initial greeting sent")
                
                # Handle conversation using Google's approach
                await asyncio.gather(
                    self.handle_frontend_messages(websocket, session, connection_id),
                    self.handle_gemini_responses(websocket, session, connection_id)
                )
                
        except Exception as e:
            logger.error(f"❌ Client #{connection_id} error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            logger.info(f"🧹 Client #{connection_id} cleanup complete")

    async def handle_frontend_messages(self, websocket, session, connection_id):
        """Handle messages from frontend using Google's approach"""
        message_count = 0
        
        try:
            async for message in websocket:
                message_count += 1
                
                try:
                    data = json.loads(message)
                    msg_type = data.get("type", "unknown")
                    
                    if msg_type == "text":
                        user_text = data.get("text", "")
                        logger.info(f"💬 Client #{connection_id} message #{message_count}: {user_text}")
                        
                        # Use new API method
                        await session.send_client_content(
                            turns=[{"role": "user", "parts": [{"text": user_text}]}], 
                            turn_complete=True
                        )
                        
                    elif msg_type == "audio_continuous":
                        try:
                            audio_data = base64.b64decode(data["data"])
                            if len(audio_data) > 100:  # Only process non-trivial audio
                                logger.debug(f"🎤 Client #{connection_id} processing audio: {len(audio_data)} bytes")
                                
                                # Use new API method for audio
                                await session.send_realtime_input(
                                    audio={"data": audio_data, "mime_type": "audio/pcm"}
                                )
                                
                        except Exception as e:
                            logger.error(f"❌ Audio processing error: {e}")
                    
                    elif msg_type == "heartbeat":
                        # Respond to heartbeat
                        await websocket.send(json.dumps({"type": "heartbeat_ack"}))
                        
                except json.JSONDecodeError as e:
                    logger.error(f"❌ JSON decode error: {e}")
                    
        except Exception as e:
            logger.error(f"❌ Frontend handler error: {e}")

    async def handle_gemini_responses(self, websocket, session, connection_id):
        """Handle Gemini responses using Google's approach"""
        try:
            # Correct Google Live API approach
            async for response in session.receive():
                logger.debug(f"📨 Client #{connection_id} received response from Gemini")
                
                if response.data is not None:
                    # Audio response
                    logger.debug(f"🗣️ Client #{connection_id} Robin audio: {len(response.data)} bytes")
                    
                    audio_b64 = base64.b64encode(response.data).decode()
                    await websocket.send(json.dumps({
                        "type": "audio",
                        "data": audio_b64
                    }))
                    
                if response.text is not None:
                    # Text response
                    logger.info(f"💭 Client #{connection_id} Robin text: {response.text}")
                    await websocket.send(json.dumps({
                        "type": "text",
                        "text": response.text
                    }))
                
                # Check for turn completion
                if hasattr(response, 'turn_complete') and response.turn_complete:
                    logger.info(f"✅ Client #{connection_id} turn complete")
                    await websocket.send(json.dumps({
                        "type": "turn_complete"
                    }))
                
        except Exception as e:
            logger.error(f"❌ Gemini response handler error: {e}")

async def main():
    """Start Google official server"""
    agent = GoogleOfficialAgent()
    
    logger.info("🚀 Starting Google Official Live API Server")
    
    # Start server with stability settings
    async with websockets.serve(
        agent.handle_connection, 
        "localhost", 
        8765,
        ping_interval=20,
        ping_timeout=10,
        close_timeout=5
    ):
        logger.info("✅ Google official server ready on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())