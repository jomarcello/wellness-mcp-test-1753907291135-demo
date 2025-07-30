#!/usr/bin/env python3
"""
Official Gemini Native Audio Dialog Server
Based on Get_started_LiveAPI_NativeAudio.py from cookbook
"""
import os
import asyncio
import base64
import json
import logging
import websockets
import pyaudio
from google import genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration
os.environ["GEMINI_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

# Official configuration from cookbook
MODEL = "gemini-2.5-flash-preview-native-audio-dialog"
CONFIG = {"response_modalities": ["AUDIO"]}

# Audio format (official)
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

class OfficialVoiceAgent:
    def __init__(self):
        self.client = genai.Client()
        
    async def handle_connection(self, websocket, path):
        """Handle WebSocket connection - official pattern"""
        logger.info("Frontend connected")
        
        try:
            async with self.client.aio.live.connect(model=MODEL, config=CONFIG) as session:
                logger.info("Connected to Gemini Live API")
                
                # Send initial greeting
                await session.send(input="สวัสดีค่ะ ยินดีต้อนรับสู่ BeautyMed Clinic", end_of_turn=True)
                
                # Run concurrent tasks (official pattern)
                await asyncio.gather(
                    self.listen_audio(session),
                    self.send_realtime(session),
                    self.receive_audio(session, websocket),
                    self.play_audio(session),
                    self.handle_frontend_messages(websocket, session)
                )
                
        except Exception as e:
            logger.error(f"Connection error: {e}")
            await websocket.send(json.dumps({"type": "error", "message": str(e)}))

    async def listen_audio(self, session):
        """Listen to microphone - official pattern"""
        pya = pyaudio.PyAudio()
        try:
            mic_info = pya.get_default_input_device_info()
            stream = pya.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=SEND_SAMPLE_RATE,
                input=True,
                input_device_index=mic_info["index"],
                frames_per_buffer=CHUNK_SIZE,
            )
            
            while True:
                data = stream.read(CHUNK_SIZE)
                await session.send_realtime_input(audio={"data": data, "mime_type": "audio/pcm"})
                await asyncio.sleep(0.01)  # Small delay
                
        except Exception as e:
            logger.error(f"Audio input error: {e}")
        finally:
            if 'stream' in locals():
                stream.close()
            pya.terminate()

    async def send_realtime(self, session):
        """Send real-time audio - official pattern"""
        # This is handled by listen_audio method
        pass

    async def receive_audio(self, session, websocket):
        """Receive audio from Gemini - official pattern"""
        try:
            async for response in session.receive():
                if response.data is not None:
                    # Send to frontend for playback
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
                    
        except Exception as e:
            logger.error(f"Receive audio error: {e}")

    async def play_audio(self, session):
        """Play audio responses - official pattern"""
        # Audio playback is handled by frontend
        pass

    async def handle_frontend_messages(self, websocket, session):
        """Handle frontend messages"""
        try:
            async for message in websocket:
                data = json.loads(message)
                
                if data.get("type") == "text":
                    await session.send(input=data["text"], end_of_turn=True)
                    
        except Exception as e:
            logger.error(f"Frontend message error: {e}")

async def main():
    """Start the official voice agent"""
    agent = OfficialVoiceAgent()
    
    async with websockets.serve(agent.handle_connection, "localhost", 8765):
        logger.info("Official voice agent started on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())