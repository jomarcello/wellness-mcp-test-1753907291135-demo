#!/usr/bin/env python3
"""
Final Working Conversational Voice Agent
Based on working cookbook example
"""
import asyncio
import sys
import traceback
import os
import json
import logging
import websockets
import base64
import pyaudio
from google import genai

if sys.version_info < (3, 11, 0):
    import taskgroup, exceptiongroup
    asyncio.TaskGroup = taskgroup.TaskGroup
    asyncio.ExceptionGroup = exceptiongroup.ExceptionGroup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration - CRITICAL: Set environment variable
os.environ["GOOGLE_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

# Official configuration from cookbook
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

pya = pyaudio.PyAudio()

# Initialize client AFTER setting environment variable
client = genai.Client()

MODEL = "gemini-2.5-flash-preview-native-audio-dialog"
CONFIG = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic คลินิกความงาม ตอบเป็นภาษาไทยเท่านั้น"
}

class FinalAudioLoop:
    def __init__(self, websocket):
        self.websocket = websocket
        self.audio_in_queue = None
        self.out_queue = None
        self.session = None
        self.audio_stream = None
        self.running = True

    async def listen_audio(self):
        """Listen to microphone - exact cookbook pattern"""
        mic_info = pya.get_default_input_device_info()
        self.audio_stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=SEND_SAMPLE_RATE,
            input=True,
            input_device_index=mic_info["index"],
            frames_per_buffer=CHUNK_SIZE,
        )
        
        kwargs = {"exception_on_overflow": False} if __debug__ else {}
        
        while self.running:
            try:
                data = await asyncio.to_thread(self.audio_stream.read, CHUNK_SIZE, **kwargs)
                await self.out_queue.put({"data": data, "mime_type": "audio/pcm"})
            except Exception as e:
                logger.error(f"Audio input error: {e}")
                break

    async def send_realtime(self):
        """Send real-time audio - exact cookbook pattern"""
        while self.running:
            try:
                msg = await self.out_queue.get()
                await self.session.send_realtime_input(audio=msg)
            except Exception as e:
                logger.error(f"Send realtime error: {e}")
                break

    async def receive_audio(self):
        """Receive audio - exact cookbook pattern + WebSocket"""
        while self.running:
            try:
                turn = self.session.receive()
                async for response in turn:
                    if data := response.data:
                        # Send to WebSocket frontend
                        await self.websocket.send(json.dumps({
                            "type": "audio",
                            "data": base64.b64encode(data).decode()
                        }))
                        continue
                        
                    if text := response.text:
                        logger.info(f"Text: {text}")
                        await self.websocket.send(json.dumps({
                            "type": "text",
                            "text": text
                        }))

                    # Handle interruptions - exact cookbook pattern
                    while not self.audio_in_queue.empty():
                        self.audio_in_queue.get_nowait()
                        
            except Exception as e:
                logger.error(f"Receive audio error: {e}")
                break

    async def handle_frontend_messages(self):
        """Handle text messages from frontend"""
        try:
            async for message in self.websocket:
                if not self.running:
                    break
                    
                data = json.loads(message)
                if data.get("type") == "text":
                    await self.session.send(input=data["text"], end_of_turn=True)
                    
        except Exception as e:
            logger.error(f"Frontend message error: {e}")
            self.running = False

    async def run(self):
        """Run the audio loop - exact cookbook pattern"""
        try:
            async with (
                client.aio.live.connect(model=MODEL, config=CONFIG) as session,
                asyncio.TaskGroup() as tg,
            ):
                self.session = session
                self.audio_in_queue = asyncio.Queue()
                self.out_queue = asyncio.Queue(maxsize=5)
                
                logger.info("✅ Connected to Gemini Live API")
                
                # Send initial greeting
                await session.send(input="สวัสดีค่ะ ยินดีต้อนรับสู่ BeautyMed Clinic", end_of_turn=True)
                
                # Create all tasks - exact cookbook pattern
                tg.create_task(self.send_realtime())
                tg.create_task(self.listen_audio())
                tg.create_task(self.receive_audio())
                tg.create_task(self.handle_frontend_messages())
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Audio loop error: {e}")
            traceback.print_exc()
        finally:
            self.running = False
            if self.audio_stream:
                self.audio_stream.close()

async def handle_connection(websocket, path):
    """Handle WebSocket connection"""
    logger.info("Frontend connected")
    
    try:
        audio_loop = FinalAudioLoop(websocket)
        await audio_loop.run()
        
    except Exception as e:
        logger.error(f"Connection error: {e}")
        traceback.print_exc()
    finally:
        logger.info("Frontend disconnected")

async def main():
    """Start the final voice agent"""
    logger.info("Starting Final Conversational Voice Agent")
    
    async with websockets.serve(handle_connection, "localhost", 8765):
        logger.info("✅ Final voice agent started on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())