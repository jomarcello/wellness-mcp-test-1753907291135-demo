#!/usr/bin/env python3
"""
Stable Conversational Voice Agent - Connection Stability Focused
"""
import asyncio
import os
import json
import logging
import websockets
import base64
from google import genai
import signal
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration
os.environ["GOOGLE_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

# Configuration - Using proven stable model
MODEL = "models/gemini-2.0-flash-live-001"
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

class StableConversationalAgent:
    def __init__(self):
        self.is_listening = True
        self.is_speaking = False
        self.connection_count = 0
        self.heartbeat_interval = 30  # Send heartbeat every 30 seconds
        
    async def handle_connection(self, websocket):
        """Handle conversational connection with stability measures"""
        self.connection_count += 1
        connection_id = self.connection_count
        logger.info(f"👋 Client #{connection_id} connected for conversation")
        
        # Set connection parameters for stability
        websocket.ping_interval = 20
        websocket.ping_timeout = 10
        websocket.close_timeout = 5
        
        gemini_session = None
        heartbeat_task = None
        
        try:
            client = genai.Client()
            
            async with client.aio.live.connect(model=MODEL, config=CONFIG) as session:
                gemini_session = session
                logger.info(f"✅ Client #{connection_id} connected to Gemini")
                
                # Start heartbeat to keep connection alive
                heartbeat_task = asyncio.create_task(self.heartbeat(websocket, connection_id))
                
                # Send initial greeting using newer API method
                await session.send_client_content(
                    turns=[{"role": "user", "parts": [{"text": "สวัสดีค่ะ"}]}], 
                    turn_complete=True
                )
                logger.info(f"🗣️ Client #{connection_id}: Initial greeting sent")
                
                # Set initial listening state - Robin will speak first
                self.is_listening = False
                self.is_speaking = True
                
                # Handle conversation with timeout protection
                await asyncio.wait_for(
                    asyncio.gather(
                        self.handle_frontend(websocket, session, connection_id),
                        self.handle_gemini(websocket, session, connection_id)
                    ),
                    timeout=None  # No overall timeout, but individual operations have timeouts
                )
                
        except websockets.exceptions.ConnectionClosed as e:
            logger.warning(f"🔌 Client #{connection_id} disconnected: {e}")
        except asyncio.TimeoutError:
            logger.error(f"⏰ Client #{connection_id} timeout")
        except Exception as e:
            logger.error(f"❌ Client #{connection_id} error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Cleanup
            if heartbeat_task:
                heartbeat_task.cancel()
            logger.info(f"🧹 Client #{connection_id} cleanup complete")

    async def heartbeat(self, websocket, connection_id):
        """Send periodic heartbeat to keep connection alive"""
        try:
            while True:
                await asyncio.sleep(self.heartbeat_interval)
                if websocket.closed:
                    break
                    
                try:
                    await asyncio.wait_for(
                        websocket.send(json.dumps({"type": "heartbeat"})),
                        timeout=5
                    )
                    logger.debug(f"💓 Heartbeat sent to client #{connection_id}")
                except Exception as e:
                    logger.warning(f"💔 Heartbeat failed for client #{connection_id}: {e}")
                    break
                    
        except asyncio.CancelledError:
            logger.debug(f"💓 Heartbeat cancelled for client #{connection_id}")

    async def handle_frontend(self, websocket, session, connection_id):
        """Handle frontend messages with error resilience"""
        message_count = 0
        
        try:
            async for message in websocket:
                message_count += 1
                
                try:
                    # Add timeout for message processing
                    await asyncio.wait_for(
                        self.process_message(message, session, connection_id, message_count),
                        timeout=10
                    )
                except asyncio.TimeoutError:
                    logger.error(f"⏰ Message #{message_count} timeout for client #{connection_id}")
                except Exception as e:
                    logger.error(f"❌ Message #{message_count} error for client #{connection_id}: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"🔌 Frontend connection closed for client #{connection_id}")
        except Exception as e:
            logger.error(f"❌ Frontend error for client #{connection_id}: {e}")

    async def process_message(self, message, session, connection_id, message_count):
        """Process individual message with timeout protection"""
        try:
            data = json.loads(message)
            msg_type = data.get("type", "unknown")
            
            if msg_type == "text":
                user_text = data.get("text", "")
                logger.info(f"💬 Client #{connection_id} message #{message_count}: {user_text}")
                self.is_listening = False
                
                # Use new API method
                await session.send_client_content(
                    turns=[{"role": "user", "parts": [{"text": user_text}]}], 
                    turn_complete=True
                )
                
            elif msg_type == "audio_continuous":
                if self.is_listening:
                    try:
                        audio_data = base64.b64decode(data["data"])
                        if len(audio_data) > 100:  # Only process non-trivial audio
                            logger.info(f"🎤 Client #{connection_id} processing audio chunk: {len(audio_data)} bytes")
                            await session.send_realtime_input(
                                audio={"data": audio_data, "mime_type": "audio/pcm"}
                            )
                    except Exception as e:
                        logger.error(f"❌ Audio processing error: {e}")
                else:
                    logger.debug(f"🔇 Client #{connection_id} ignoring audio - not listening (listening={self.is_listening}, speaking={self.is_speaking})")
                    
            elif msg_type == "start_listening":
                self.is_listening = True
                logger.info(f"👂 Client #{connection_id} listening mode ON")
                
            elif msg_type == "stop_listening":
                self.is_listening = False
                logger.info(f"🔇 Client #{connection_id} listening mode OFF")
                
            elif msg_type == "heartbeat":
                # Client heartbeat response - ignore
                pass
            else:
                logger.debug(f"🤷 Unknown message type from client #{connection_id}: {msg_type}")
                
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON decode error for client #{connection_id}: {e}")

    async def handle_gemini(self, websocket, session, connection_id):
        """Handle Gemini responses with connection stability"""
        response_count = 0
        
        try:
            async for response in session.receive():
                response_count += 1
                
                try:
                    # Process response with timeout
                    await asyncio.wait_for(
                        self.process_gemini_response(response, websocket, connection_id, response_count),
                        timeout=15
                    )
                except asyncio.TimeoutError:
                    logger.error(f"⏰ Gemini response #{response_count} timeout for client #{connection_id}")
                except Exception as e:
                    logger.error(f"❌ Gemini response #{response_count} error for client #{connection_id}: {e}")
                    
        except Exception as e:
            logger.error(f"❌ Gemini handler error for client #{connection_id}: {e}")

    async def process_gemini_response(self, response, websocket, connection_id, response_count):
        """Process individual Gemini response"""
        if response.data is not None:
            # Robin is speaking - stop listening
            self.is_speaking = True
            self.is_listening = False
            
            logger.info(f"🗣️ Client #{connection_id} Robin speaking: {len(response.data)} bytes (response #{response_count})")
            
            await websocket.send(json.dumps({
                "type": "audio",
                "data": base64.b64encode(response.data).decode()
            }))
            
        if response.text is not None:
            logger.info(f"💭 Client #{connection_id} Robin text: {response.text}")
            await websocket.send(json.dumps({
                "type": "text", 
                "text": response.text
            }))
            
        # Check if turn is complete
        if hasattr(response, 'turn_complete') and response.turn_complete:
            # Robin finished speaking - resume listening
            self.is_speaking = False
            self.is_listening = True
            logger.info(f"✅ Client #{connection_id} turn complete - resuming listening")
            
            await websocket.send(json.dumps({
                "type": "turn_complete"
            }))
            
            # Log listening state for debugging
            logger.info(f"🎧 Client #{connection_id} listening state: {self.is_listening}")

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"🛑 Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

async def main():
    """Start stable conversational server"""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    agent = StableConversationalAgent()
    
    logger.info("🚀 Starting Stable Conversational Agent")
    
    # Configure server with connection stability settings
    async with websockets.serve(
        agent.handle_connection, 
        "localhost", 
        8765,
        ping_interval=20,
        ping_timeout=10,
        close_timeout=5,
        max_size=10 * 1024 * 1024,  # 10MB max message size
        compression=None  # Disable compression for audio
    ):
        logger.info("✅ Stable conversational agent ready on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())