#!/usr/bin/env python3
"""
Official Google Gemini Conversational Voice Agent
Based on Get_started_LiveAPI_NativeAudio.py
"""
import os
import asyncio
import base64
import json
import logging
import websockets
import pyaudio
from google import genai

# Configure logging with detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API Configuration
os.environ["GEMINI_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

# Official configuration
MODEL = "gemini-2.5-flash-preview-native-audio-dialog"
CONFIG = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic คลินิกความงาม ตอบเป็นภาษาไทยเท่านั้น"
}

# Audio format (official)
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

class ConversationalVoiceAgent:
    def __init__(self):
        self.client = genai.Client()
        self.audio_in_queue = None
        self.out_queue = None
        self.audio_stream = None
        self.running = False
        self.websocket = None
        
    def inspect_response(self, response):
        """Inspect response object for user transcriptions"""
        try:
            # Full debug inspection
            if hasattr(response, '__dict__'):
                attrs = response.__dict__
                logger.debug(f"📋 Response type: {type(response)}")
                logger.debug(f"📋 Response attributes: {list(attrs.keys())}")
                
                # Log all non-empty attributes for debugging
                for key, value in attrs.items():
                    if value is not None:
                        logger.debug(f"📋 {key}: {type(value)} = {repr(value)[:200]}...")
                
                # Look for text, transcript, or user-related content
                for key, value in attrs.items():
                    if value and ('text' in key.lower() or 'transcript' in key.lower() or 'user' in key.lower()):
                        logger.info(f"👤 Found user content in {key}: {value}")
                        
            # Check specific known attributes
            if hasattr(response, 'client_content') and response.client_content:
                logger.info("📥 Client content found")
                client_content = response.client_content
                logger.debug(f"📥 Client content type: {type(client_content)}")
                
                if hasattr(client_content, 'turns') and client_content.turns:
                    logger.info(f"📥 Found {len(client_content.turns)} turns")
                    for i, turn in enumerate(client_content.turns):
                        logger.debug(f"📥 Turn {i}: {type(turn)}")
                        if hasattr(turn, 'role'):
                            logger.info(f"📥 Turn {i} role: {turn.role}")
                            if turn.role == 'user':
                                logger.info("👤 User turn detected!")
                                if hasattr(turn, 'parts'):
                                    for j, part in enumerate(turn.parts):
                                        logger.debug(f"👤 Part {j}: {type(part)}")
                                        if hasattr(part, 'text'):
                                            logger.info(f"👤 USER SAID: {part.text}")
                                            # Send user transcript to frontend
                                            if self.websocket:
                                                asyncio.create_task(self.send_user_transcript(part.text))
                                                
            # Check for server content as well
            if hasattr(response, 'server_content') and response.server_content:
                logger.debug("📥 Server content found")
                server_content = response.server_content
                logger.debug(f"📥 Server content type: {type(server_content)}")
                
                # Check for any user-related content in server_content
                if hasattr(server_content, '__dict__'):
                    for key, value in server_content.__dict__.items():
                        if value and 'user' in key.lower():
                            logger.info(f"👤 Server content user data in {key}: {value}")
                                        
        except Exception as e:
            logger.debug(f"Error inspecting response: {e}")
    
    async def send_user_transcript(self, text):
        """Send user transcription to frontend"""
        try:
            if self.websocket and not self.websocket.closed:
                message = {
                    "type": "user_transcript",
                    "text": text
                }
                await self.websocket.send(json.dumps(message))
                logger.info(f"📤 Sent user transcript to frontend: {text}")
        except Exception as e:
            logger.error(f"Error sending user transcript: {e}")
        
    async def handle_frontend_connection(self, websocket, path):
        """Real-time conversational handling"""
        logger.info("Frontend connected")
        self.websocket = websocket
        
        try:
            async with self.client.aio.live.connect(model=MODEL, config=CONFIG) as session:
                self.audio_in_queue = asyncio.Queue()
                self.out_queue = asyncio.Queue(maxsize=5)
                self.running = True
                
                # Start conversation
                await session.send(input="สวัสดีค่ะ ยินดีต้อนรับสู่ BeautyMed Clinic", end_of_turn=True)
                
                # Run concurrent tasks for smooth audio
                tasks = [
                    asyncio.create_task(self.handle_audio_input(session)),
                    asyncio.create_task(self.handle_audio_output(session)),
                    asyncio.create_task(self.handle_frontend_messages(websocket, session))
                ]
                
                await asyncio.gather(*tasks)
                
        except Exception as e:
            logger.error(f"Connection error: {e}")
            await websocket.send(json.dumps({"type": "error", "message": str(e)}))
        finally:
            self.running = False

    async def handle_audio_input(self, session):
        """Continuous audio input - official pattern"""
        pya = pyaudio.PyAudio()
        try:
            mic_info = pya.get_default_input_device_info()
            logger.info(f"🎤 Using microphone: {mic_info['name']}")
            logger.info(f"🎤 Sample rate: {SEND_SAMPLE_RATE}Hz, Channels: {CHANNELS}")
            
            stream = pya.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=SEND_SAMPLE_RATE,
                input=True,
                input_device_index=mic_info["index"],
                frames_per_buffer=CHUNK_SIZE
            )
            logger.info("🎤 Microphone stream opened successfully")
            
            logger.info("Audio input stream started - listening for speech")
            chunk_count = 0
            
            while self.running:
                try:
                    data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
                    chunk_count += 1
                    
                    if chunk_count % 50 == 0:  # Log every 50 chunks (~1 second)
                        logger.info(f"🎤 Audio input active - processed {chunk_count} chunks ({len(data)} bytes per chunk)")
                    
                    # Send audio to Gemini Live API
                    await session.send_realtime_input(audio={"data": data, "mime_type": "audio/pcm"})
                    
                    if chunk_count % 100 == 0:  # Every 2 seconds
                        logger.debug(f"🎤 Sent audio chunk {chunk_count} to Gemini Live API")
                    
                except Exception as e:
                    logger.error(f"Audio input error: {e}")
                    break
                    
        except Exception as e:
            logger.error(f"Audio input setup error: {e}")
        finally:
            if 'stream' in locals():
                stream.close()
            pya.terminate()

    async def handle_audio_output(self, session):
        """Continuous audio output - official pattern"""
        pya = pyaudio.PyAudio()
        try:
            stream = pya.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RECEIVE_SAMPLE_RATE,
                output=True
            )
            
            logger.info("Audio output stream started - ready to play responses")
            
            async for response in session.receive():
                if not self.running:
                    break
                
                # Inspect response for transcriptions
                self.inspect_response(response)
                
                if response.data is not None:
                    stream.write(response.data)
                    logger.debug(f"🔊 Played audio chunk: {len(response.data)} bytes")
                    
                if response.text is not None:
                    logger.info(f"🗣️  Agent says: {response.text}")
                    
                # Check for turn completion
                if hasattr(response, 'turn_complete') and response.turn_complete:
                    logger.info("🔄 Turn completed - conversation ready for next input")
                    
        except Exception as e:
            logger.error(f"Audio output error: {e}")
        finally:
            if 'stream' in locals():
                stream.close()
            pya.terminate()

    async def handle_frontend_messages(self, websocket, session):
        """Handle text messages from frontend"""
        try:
            async for message in websocket:
                if not self.running:
                    break
                    
                data = json.loads(message)
                if data.get("type") == "text":
                    await session.send(input=data["text"], end_of_turn=True)
                elif data.get("type") == "stop":
                    self.running = False
                    break
                # Ignore audio_continuous messages - handled by direct audio streaming
                elif data.get("type") == "audio_continuous":
                    continue
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info("Frontend WebSocket closed")
            self.running = False
        except Exception as e:
            logger.error(f"Error handling frontend messages: {e}")
            self.running = False

async def main():
    """Start the conversational voice agent"""
    agent = ConversationalVoiceAgent()
    
    logger.info("Starting Conversational Voice Agent")
    logger.info("Server will run on ws://localhost:8766")
    
    try:
        async with websockets.serve(
            agent.handle_frontend_connection, 
            "localhost", 
            8766,
            ping_interval=None,
            ping_timeout=None
        ):
            logger.info("Conversational voice agent started on ws://localhost:8766")
            await asyncio.Future()  # Run forever
            
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())