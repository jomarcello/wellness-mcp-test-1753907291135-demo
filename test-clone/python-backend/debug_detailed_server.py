#!/usr/bin/env python3
"""
Debug Detailed Server - Trace Every Step
"""
import asyncio
import os
import json
import logging
import websockets
import base64
from google import genai

# Configure detailed logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# API Configuration
os.environ["GOOGLE_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

MODEL = "models/gemini-2.0-flash-live-001"
CONFIG = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "You are Robin, a friendly assistant. Respond briefly in Thai."
}

class DebugAgent:
    def __init__(self):
        self.message_count = 0
        self.audio_chunks_received = 0
        self.text_messages_received = 0
        
    async def handle_connection(self, websocket):
        """Handle connection with detailed logging"""
        logger.info("🔌 NEW CLIENT CONNECTED")
        client_ip = websocket.remote_address
        logger.info(f"📍 Client IP: {client_ip}")
        
        try:
            client = genai.Client()
            logger.info("🤖 Created Gemini client")
            
            async with client.aio.live.connect(model=MODEL, config=CONFIG) as session:
                logger.info("✅ GEMINI LIVE SESSION ESTABLISHED")
                
                # Start listening for messages
                await self.handle_messages(websocket, session)
                
        except Exception as e:
            logger.error(f"❌ CONNECTION ERROR: {e}")
            import traceback
            traceback.print_exc()

    async def handle_messages(self, websocket, session):
        """Handle messages with detailed logging"""
        logger.info("👂 STARTED LISTENING FOR MESSAGES")
        
        try:
            async for message in websocket:
                self.message_count += 1
                logger.info(f"📨 MESSAGE #{self.message_count} RECEIVED")
                logger.info(f"📦 Raw message length: {len(message)} bytes")
                
                try:
                    data = json.loads(message)
                    msg_type = data.get("type", "unknown")
                    logger.info(f"🏷️ Message type: {msg_type}")
                    
                    if msg_type == "text":
                        self.text_messages_received += 1
                        user_text = data.get("text", "")
                        logger.info(f"💬 TEXT MESSAGE #{self.text_messages_received}: '{user_text}'")
                        
                        # Send to Gemini
                        logger.info("📤 Sending text to Gemini...")
                        await session.send(input=user_text, end_of_turn=True)
                        logger.info("✅ Text sent to Gemini successfully")
                        
                        # Start listening for Gemini response
                        await self.handle_gemini_response(websocket, session)
                        
                    elif msg_type == "audio_continuous":
                        self.audio_chunks_received += 1
                        audio_data_b64 = data.get("data", "")
                        logger.info(f"🎤 AUDIO CHUNK #{self.audio_chunks_received}")
                        logger.info(f"📊 Base64 length: {len(audio_data_b64)} chars")
                        
                        try:
                            # Decode audio
                            audio_bytes = base64.b64decode(audio_data_b64)
                            logger.info(f"🔊 Decoded audio: {len(audio_bytes)} bytes")
                            
                            # Send to Gemini
                            logger.info("📤 Sending audio to Gemini...")
                            await session.send_realtime_input(
                                audio={"data": audio_bytes, "mime_type": "audio/pcm"}
                            )
                            logger.info("✅ Audio sent to Gemini successfully")
                            
                        except Exception as audio_error:
                            logger.error(f"❌ AUDIO PROCESSING ERROR: {audio_error}")
                            
                    else:
                        logger.warning(f"⚠️ UNKNOWN MESSAGE TYPE: {msg_type}")
                        
                except json.JSONDecodeError as json_error:
                    logger.error(f"❌ JSON DECODE ERROR: {json_error}")
                    logger.error(f"📝 Raw message: {message[:200]}...")
                    
        except Exception as e:
            logger.error(f"❌ MESSAGE HANDLING ERROR: {e}")
            import traceback
            traceback.print_exc()

    async def handle_gemini_response(self, websocket, session):
        """Handle Gemini responses with detailed logging"""
        logger.info("👂 LISTENING FOR GEMINI RESPONSE...")
        
        try:
            response_count = 0
            async for response in session.receive():
                response_count += 1
                logger.info(f"📨 GEMINI RESPONSE #{response_count}")
                
                if response.data is not None:
                    logger.info(f"🔊 Audio response: {len(response.data)} bytes")
                    
                    # Send audio to frontend
                    audio_b64 = base64.b64encode(response.data).decode()
                    await websocket.send(json.dumps({
                        "type": "audio",
                        "data": audio_b64
                    }))
                    logger.info("📤 Audio sent to frontend")
                    
                if response.text is not None:
                    logger.info(f"💬 Text response: '{response.text}'")
                    await websocket.send(json.dumps({
                        "type": "text",
                        "text": response.text
                    }))
                    logger.info("📤 Text sent to frontend")
                
                # Check for turn completion
                if hasattr(response, 'turn_complete') and response.turn_complete:
                    logger.info("✅ TURN COMPLETE - Breaking response loop")
                    break
                    
        except Exception as e:
            logger.error(f"❌ GEMINI RESPONSE ERROR: {e}")
            import traceback
            traceback.print_exc()

async def main():
    """Start debug server"""
    logger.info("🚀 STARTING DEBUG DETAILED SERVER")
    agent = DebugAgent()
    
    async with websockets.serve(agent.handle_connection, "localhost", 8765):
        logger.info("✅ DEBUG SERVER READY ON ws://localhost:8765")
        logger.info("🔍 FULL LOGGING ENABLED - Every step will be traced")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())