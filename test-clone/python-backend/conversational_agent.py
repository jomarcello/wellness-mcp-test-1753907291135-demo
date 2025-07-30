#!/usr/bin/env python3
"""
Official Google Gemini Conversational Voice Agent
Based on Get_started_LiveAPI_NativeAudio.py
Real-time streaming with smooth audio
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

# Set API key
os.environ["GEMINI_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

# Official configuration
MODEL = "models/gemini-2.5-flash-preview-native-audio-dialog"
CONFIG = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic คลินิกความงาม ตอบเป็นภาษาไทยเท่านั้น พูดธรรมชาติเหมือนการสนทนา"
}

# Audio format (official specs)
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

class ConversationalVoiceAgent:
    def __init__(self):
        self.client = genai.Client(
            http_options={"api_version": "v1beta"},
            api_key=os.environ.get("GEMINI_API_KEY")
        )
        self.audio_in_queue = None
        self.out_queue = None
        self.audio_stream = None
        self.frontend_ws = None
        
    async def handle_frontend_connection(self, websocket, path):
        """Real-time conversational handling"""
        self.frontend_ws = websocket
        logger.info(f"Frontend connected: {websocket.remote_address}")
        
        try:
            async with self.client.aio.live.connect(model=MODEL, config=CONFIG) as session:
                self.audio_in_queue = asyncio.Queue()
                self.out_queue = asyncio.Queue(maxsize=5)
                
                logger.info("Connected to Gemini Live API")
                
                # Start conversation immediately
                await session.send(input="สวัสดีค่ะ ยินดีต้อนรับสู่ BeautyMed Clinic", end_of_turn=True)
                
                # Run concurrent tasks for smooth audio (official pattern)
                tasks = [
                    asyncio.create_task(self.handle_audio_input(session)),
                    asyncio.create_task(self.handle_audio_output(session, websocket)),
                    asyncio.create_task(self.handle_frontend_messages(websocket, session))
                ]
                
                await asyncio.gather(*tasks, return_exceptions=True)
                
        except Exception as e:
            logger.error(f"Connection error: {e}")
            await websocket.send(json.dumps({"type": "error", "message": str(e)}))
        finally:
            logger.info("Frontend disconnected")

    async def handle_audio_input(self, session):
        """Continuous audio input - official pattern"""
        pya = pyaudio.PyAudio()
        
        try:
            mic_info = pya.get_default_input_device_info()
            
            stream = pya.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=SEND_SAMPLE_RATE,
                input=True,
                input_device_index=mic_info["index"],
                frames_per_buffer=CHUNK_SIZE
            )
            
            logger.info("Started continuous audio input")
            
            while True:
                try:
                    data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
                    await self.out_queue.put({"data": data, "mime_type": "audio/pcm"})
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Audio input error: {e}")
                    break
                    
        except Exception as e:
            logger.error(f"Failed to start audio input: {e}")
        finally:
            try:
                stream.close()
            except:
                pass
            pya.terminate()

    async def send_realtime(self, session):
        """Real-time streaming - official pattern"""
        try:
            while True:
                msg = await self.out_queue.get()
                await session.send(input=msg["data"])
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Send realtime error: {e}")

    async def handle_audio_output(self, session, websocket):
        """Continuous audio output - official pattern"""
        pya = pyaudio.PyAudio()
        
        try:
            stream = pya.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RECEIVE_SAMPLE_RATE,
                output=True
            )
            
            logger.info("Started continuous audio output")
            
            async for response in session.receive():
                if response.data is not None:
                    # Play directly to speakers (official pattern)
                    stream.write(response.data)
                    
                    # Also send to frontend for display
                    await websocket.send(json.dumps({
                        "type": "audio_streaming",
                        "data": base64.b64encode(response.data).decode(),
                        "streaming": True
                    }))
                    
                if response.text is not None:
                    logger.info(f"Text: {response.text}")
                    await websocket.send(json.dumps({
                        "type": "text",
                        "text": response.text
                    }))
                    
        except Exception as e:
            logger.error(f"Audio output error: {e}")
        finally:
            try:
                stream.close()
            except:
                pass
            pya.terminate()

    async def handle_frontend_messages(self, websocket, session):
        """Handle text messages from frontend"""
        try:
            async for message in websocket:
                data = json.loads(message)
                logger.info(f"Frontend message: {data.get('type')}")
                
                if data.get("type") == "text":
                    await session.send(input=data["text"], end_of_turn=True)
                elif data.get("type") == "start_conversation":
                    await session.send(input="เริ่มการสนทนาใหม่", end_of_turn=True)
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info("Frontend disconnected")
        except Exception as e:
            logger.error(f"Frontend message error: {e}")

# Run the server
async def main():
    agent = ConversationalVoiceAgent()
    
    logger.info("Starting Official Google Gemini Conversational Voice Agent")
    logger.info("Server running on ws://localhost:8765")
    logger.info("Real-time streaming with smooth audio playback")
    
    try:
        async with websockets.serve(
            agent.handle_frontend_connection, 
            "localhost", 
            8765,
            ping_interval=20,
            ping_timeout=10,
            max_size=10**7
        ):
            logger.info("Conversational voice agent started!")
            await asyncio.Future()  # Run forever
            
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())