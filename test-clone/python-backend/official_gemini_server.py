#!/usr/bin/env python3
"""
Official Gemini Live API Server - Based on Google's official example
Uses Gemini 2.5 Flash with Zephyr voice for perfect audio quality
"""
import os
import asyncio
import base64
import json
import logging
import websockets
import traceback
from google import genai
from google.genai import types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration
os.environ["GEMINI_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

# Official Google configuration
MODEL = "models/gemini-2.5-flash-preview-native-audio-dialog"

client = genai.Client(
    http_options={"api_version": "v1beta"},
    api_key=os.environ.get("GEMINI_API_KEY")
)

# Official LiveConnectConfig with proper types
CONFIG = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    media_resolution="MEDIA_RESOLUTION_MEDIUM",
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Zephyr")
        )
    ),
    system_instruction="""คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic คลินิกความงาม
ตอบเป็นภาษาไทยเท่านั้น พูดสั้นๆ กะทัดรัด และเป็นมิตร พูดช้าๆ ชัดเจน
บริการ: โบท็อกซ์, ฟิลเลอร์, รักษาสิว, ขจัดขน, ทำผิวขาว
ถามชื่อ เบอร์โทร บริการที่ต้องการ และวันเวลาที่สะดวก""",
    context_window_compression=types.ContextWindowCompressionConfig(
        trigger_tokens=25600,
        sliding_window=types.SlidingWindow(target_tokens=12800),
    ),
)

class OfficialGeminiServer:
    def __init__(self):
        self.active_connections = {}
        
    async def handle_client(self, websocket, path=None):
        """Handle client connections with official Google configuration"""
        client_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"New client connected: {client_id}")
        
        try:
            # Connect using official configuration
            async with client.aio.live.connect(model=MODEL, config=CONFIG) as session:
                self.active_connections[client_id] = {
                    'websocket': websocket,
                    'session': session,
                    'running': True
                }
                
                logger.info(f"Client {client_id} connected to Gemini 2.5 Flash Live API")
                
                # Create tasks for bidirectional communication
                tasks = [
                    asyncio.create_task(self.handle_client_messages(client_id)),
                    asyncio.create_task(self.handle_gemini_responses(client_id))
                ]
                
                # Send initial Thai greeting
                await session.send(
                    input="สวัสดีค่ะ ยินดีต้อนรับสู่ BeautyMed Clinic",
                    end_of_turn=True
                )
                
                # Wait for tasks to complete
                await asyncio.gather(*tasks, return_exceptions=True)
                
        except Exception as e:
            logger.error(f"Error handling client {client_id}: {e}")
            traceback.print_exc()
            await self.send_error_to_client(websocket, str(e))
        finally:
            # Clean up connection
            if client_id in self.active_connections:
                self.active_connections[client_id]['running'] = False
                del self.active_connections[client_id]
            logger.info(f"Client {client_id} disconnected")
    
    async def handle_client_messages(self, client_id):
        """Handle messages from client using official methods"""
        conn = self.active_connections.get(client_id)
        if not conn:
            return
            
        websocket = conn['websocket']
        session = conn['session']
        
        try:
            async for message in websocket:
                if not conn['running']:
                    break
                    
                data = json.loads(message)
                logger.info(f"Client {client_id} message: {data.get('type')}")
                
                if data.get("type") == "audio":
                    # Handle audio data using official method
                    audio_data = base64.b64decode(data["data"])
                    logger.info(f"Received audio: {len(audio_data)} bytes")
                    
                    # Send audio using deprecated but working send method
                    await session.send(input=audio_data)
                    
                elif data.get("type") == "text":
                    # Handle text input
                    text = data.get("text", "")
                    await session.send(
                        input=text,
                        end_of_turn=True
                    )
                    
                elif data.get("type") == "start_conversation":
                    # Start new conversation
                    await session.send(
                        input="เริ่มการสนทนาใหม่",
                        end_of_turn=True
                    )
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client {client_id} disconnected")
            conn['running'] = False
        except Exception as e:
            logger.error(f"Error handling messages from {client_id}: {e}")
            conn['running'] = False
    
    async def handle_gemini_responses(self, client_id):
        """Handle responses from Gemini using official receive pattern"""
        conn = self.active_connections.get(client_id)
        if not conn:
            return
            
        websocket = conn['websocket']
        session = conn['session']
        
        try:
            while conn['running']:
                turn = session.receive()
                async for response in turn:
                    if not conn['running']:
                        break
                        
                    # Send audio response with slight delay to prevent overlapping
                    if response.data is not None:
                        logger.info(f"Sending audio to {client_id}: {len(response.data)} bytes")
                        await websocket.send(json.dumps({
                            "type": "audio",
                            "data": base64.b64encode(response.data).decode()
                        }))
                        # Small delay to prevent audio overlap
                        await asyncio.sleep(0.05)
                    
                    # Send text response
                    if response.text is not None:
                        logger.info(f"Sending text to {client_id}: {response.text}")
                        await websocket.send(json.dumps({
                            "type": "text",
                            "text": response.text
                        }))
                        
        except Exception as e:
            logger.error(f"Error handling Gemini responses for {client_id}: {e}")
            conn['running'] = False
    
    async def send_error_to_client(self, websocket, error_message):
        """Send error message to client"""
        try:
            await websocket.send(json.dumps({
                "type": "error",
                "message": error_message
            }))
        except:
            pass

async def main():
    """Start the official Gemini Live API WebSocket server"""
    server = OfficialGeminiServer()
    
    logger.info("Starting Official Gemini 2.5 Flash Live API Server")
    logger.info("Server running on ws://localhost:8765")
    logger.info("Using Zephyr voice for perfect Thai audio quality")
    
    try:
        async with websockets.serve(
            server.handle_client,
            "localhost",
            8765,
            ping_interval=20,
            ping_timeout=10,
            max_size=10**7,
            compression=None
        ):
            logger.info("WebSocket server is running...")
            await asyncio.Future()  # Run forever
            
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())