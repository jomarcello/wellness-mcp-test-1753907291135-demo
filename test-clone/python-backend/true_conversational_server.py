#!/usr/bin/env python3
"""
True Conversational Voice Agent - Based on Google Cookbook Examples
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

# Configuration based on cookbook examples
MODEL = "models/gemini-2.0-flash-live-001"
CONFIG = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "You are Robin, a warm and friendly female assistant for BeautyMed Clinic in Thailand. Always respond in Thai with a caring, professional tone. Keep responses concise and natural. You help with beauty treatments, appointments, and general clinic information.",
    "speech_config": {
        "voice_config": {
            "prebuilt_voice_config": {
                "voice_name": "Aoede"
            }
        }
    }
}

class TrueConversationalAgent:
    def __init__(self):
        self.is_listening = True
        self.is_speaking = False
        self.audio_buffer = []
        self.silence_threshold = 0.01
        self.silence_duration = 0
        self.max_silence = 1.5  # seconds
        
    async def handle_connection(self, websocket):
        """Handle conversational connection"""
        logger.info("🎙️ Client connected for true conversation")
        
        try:
            client = genai.Client()
            
            async with client.aio.live.connect(model=MODEL, config=CONFIG) as session:
                logger.info("✅ Connected to Gemini Live - Ready for conversation")
                
                # Handle conversation
                await asyncio.gather(
                    self.handle_frontend(websocket, session),
                    self.handle_gemini_responses(websocket, session)
                )
                
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            import traceback
            traceback.print_exc()

    async def handle_frontend(self, websocket, session):
        """Handle frontend messages with voice activity detection"""
        try:
            async for message in websocket:
                data = json.loads(message)
                
                if data.get("type") == "text":
                    logger.info(f"💬 User text: {data['text']}")
                    await self.process_user_input(session, text=data["text"])
                    
                elif data.get("type") == "audio_continuous" and self.is_listening:
                    try:
                        audio_data = base64.b64decode(data["data"])
                        
                        # Add to buffer for voice activity detection
                        self.audio_buffer.append(audio_data)
                        
                        # Simple voice activity detection (check for non-silence)
                        if len(audio_data) > 100:  # Non-trivial audio
                            self.silence_duration = 0
                            # Send realtime audio to Gemini
                            await session.send_realtime_input(
                                audio={"data": audio_data, "mime_type": "audio/pcm"}
                            )
                        else:
                            self.silence_duration += 0.064  # ~64ms per chunk
                            
                            # If we detect silence after speech, process the turn
                            if self.silence_duration > self.max_silence and len(self.audio_buffer) > 10:
                                logger.info(f"🎤 Voice turn detected - processing {len(self.audio_buffer)} chunks")
                                await self.process_voice_turn(session)
                        
                    except Exception as e:
                        logger.error(f"❌ Audio processing error: {e}")
                        
        except Exception as e:
            logger.error(f"❌ Frontend error: {e}")

    async def process_voice_turn(self, session):
        """Process a complete voice turn"""
        if not self.audio_buffer:
            return
            
        try:
            # Stop listening while processing
            self.is_listening = False
            
            # Send turn complete to trigger response
            await session.send_client_content(
                turns=[{"role": "user", "parts": [{"text": ""}]}], 
                turn_complete=True
            )
            
            # Clear buffer
            self.audio_buffer = []
            self.silence_duration = 0
            
            logger.info("🔄 Voice turn sent to Gemini")
            
        except Exception as e:
            logger.error(f"❌ Voice turn processing error: {e}")
            self.is_listening = True

    async def process_user_input(self, session, text=""):
        """Process user input (text or voice)"""
        try:
            self.is_listening = False
            
            await session.send_client_content(
                turns=[{"role": "user", "parts": [{"text": text}]}], 
                turn_complete=True
            )
            
        except Exception as e:
            logger.error(f"❌ Input processing error: {e}")
            self.is_listening = True

    async def handle_gemini_responses(self, websocket, session):
        """Handle Gemini responses with proper turn management"""
        try:
            audio_chunks = []
            
            async for response in session.receive():
                
                if response.data is not None:
                    # Robin is speaking
                    self.is_speaking = True
                    self.is_listening = False
                    
                    # Collect audio chunks
                    audio_chunks.append(response.data)
                    logger.info(f"🗣️ Robin: {len(response.data)} bytes (chunk {len(audio_chunks)})")
                    
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
                
                # Check if this response indicates end of turn
                if hasattr(response, 'turn_complete') and response.turn_complete:
                    # Robin finished completely
                    self.is_speaking = False
                    self.is_listening = True
                    logger.info(f"✅ Robin finished speaking ({len(audio_chunks)} total chunks) - resuming listening")
                    
                    await websocket.send(json.dumps({
                        "type": "turn_complete"
                    }))
                    
                    # Reset for next turn
                    audio_chunks = []
                    break  # Important: break out of the response loop
                    
        except Exception as e:
            logger.error(f"❌ Gemini response error: {e}")
            # Ensure we resume listening on error
            self.is_speaking = False
            self.is_listening = True

async def main():
    """Start true conversational server"""
    agent = TrueConversationalAgent()
    
    logger.info("🚀 Starting True Conversational Agent")
    
    async with websockets.serve(agent.handle_connection, "localhost", 8765):
        logger.info("✅ True conversational agent ready on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())