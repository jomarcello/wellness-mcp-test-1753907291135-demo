#!/usr/bin/env python3
"""
Conversational Gemini Live API Server - Real continuous streaming like Google's site
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

MODEL = "models/gemini-2.5-flash-preview-native-audio-dialog"

client = genai.Client(
    http_options={"api_version": "v1beta"},
    api_key=os.environ.get("GEMINI_API_KEY")
)

# Conversational config - optimized for smooth streaming
CONFIG = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    media_resolution="MEDIA_RESOLUTION_HIGH",  # Higher quality
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Zephyr")
        )
    ),
    system_instruction="""คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic คลินิกความงาม
ตอบเป็นภาษาไทยเท่านั้น พูดธรรมชาติเหมือนการสนทนา ไม่ต้องรอให้คนพูดจบ
บริการ: โบท็อกซ์, ฟิลเลอร์, รักษาสิว, ขจัดขน, ทำผิวขาว
ถามชื่อ เบอร์โทร บริการที่ต้องการ และวันเวลาที่สะดวก""",
    # Enable smooth conversation flow
    generation_config=types.GenerationConfig(
        response_modalities=["AUDIO"],
        max_output_tokens=150,  # Shorter responses for natural flow
        temperature=0.8  # More natural speech
    )
)

class ConversationalGeminiServer:
    def __init__(self):
        self.active_connections = {}
        
    async def handle_client(self, websocket, path=None):
        """Handle conversational client connections"""
        client_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"New conversational client: {client_id}")
        
        try:
            # Connect with conversational config
            async with client.aio.live.connect(model=MODEL, config=CONFIG) as session:
                self.active_connections[client_id] = {
                    'websocket': websocket,
                    'session': session,
                    'running': True,
                    'audio_buffer': [],
                    'is_streaming': False
                }
                
                logger.info(f"Client {client_id} connected - conversational mode")
                
                # Create tasks for real-time communication
                tasks = [
                    asyncio.create_task(self.handle_client_messages(client_id)),
                    asyncio.create_task(self.handle_gemini_responses(client_id)),
                    asyncio.create_task(self.stream_audio_buffer(client_id))
                ]
                
                # Send initial greeting
                await session.send(
                    input="สวัสดีค่ะ ยินดีต้อนรับสู่ BeautyMed Clinic คุณต้องการปรึกษาบริการอะไรคะ",
                    end_of_turn=True
                )
                
                # Wait for tasks
                await asyncio.gather(*tasks, return_exceptions=True)
                
        except Exception as e:
            logger.error(f"Error handling conversational client {client_id}: {e}")
            traceback.print_exc()
            await self.send_error_to_client(websocket, str(e))
        finally:
            # Clean up
            if client_id in self.active_connections:
                self.active_connections[client_id]['running'] = False
                del self.active_connections[client_id]
            logger.info(f"Conversational client {client_id} disconnected")
    
    async def handle_client_messages(self, client_id):
        """Handle real-time messages from client"""
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
                
                if data.get("type") == "audio_start":
                    # User started speaking - interrupt if Gemini is talking
                    logger.info(f"User started speaking - interrupting Gemini")
                    conn['audio_buffer'] = []  # Clear buffer
                    conn['is_streaming'] = False
                    
                elif data.get("type") == "audio_chunk":
                    # Real-time audio streaming
                    audio_data = base64.b64decode(data["data"])
                    await session.send(input=audio_data)
                    
                elif data.get("type") == "audio_end":
                    # User finished speaking - signal end of turn
                    await session.send(end_of_turn=True)
                    
                elif data.get("type") == "text":
                    # Text input
                    text = data.get("text", "")
                    await session.send(input=text, end_of_turn=True)
                    
                elif data.get("type") == "start_conversation":
                    # Start conversation
                    await session.send(
                        input="เริ่มการสนทนาใหม่",
                        end_of_turn=True
                    )
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Conversational client {client_id} disconnected")
            conn['running'] = False
        except Exception as e:
            logger.error(f"Error handling messages from {client_id}: {e}")
            conn['running'] = False
    
    async def handle_gemini_responses(self, client_id):
        """Handle responses from Gemini - buffer for smooth streaming"""
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
                        
                    # Buffer audio responses for smooth playback
                    if response.data is not None:
                        logger.info(f"Buffering audio for {client_id}: {len(response.data)} bytes")
                        conn['audio_buffer'].append(response.data)
                        
                        # Start streaming if not already
                        if not conn['is_streaming']:
                            conn['is_streaming'] = True
                    
                    # Send text response immediately
                    if response.text is not None:
                        logger.info(f"Sending text to {client_id}: {response.text}")
                        await websocket.send(json.dumps({
                            "type": "text",
                            "text": response.text
                        }))
                        
        except Exception as e:
            logger.error(f"Error handling Gemini responses for {client_id}: {e}")
            conn['running'] = False
    
    async def stream_audio_buffer(self, client_id):
        """Stream audio buffer continuously for smooth playback"""
        conn = self.active_connections.get(client_id)
        if not conn:
            return
            
        websocket = conn['websocket']
        
        try:
            while conn['running']:
                if conn['is_streaming'] and conn['audio_buffer']:
                    # Get all buffered audio
                    buffered_audio = conn['audio_buffer'][:]
                    conn['audio_buffer'] = []
                    
                    # Combine all chunks into one smooth stream
                    combined_audio = b''.join(buffered_audio)
                    
                    if combined_audio:
                        logger.info(f"Streaming combined audio to {client_id}: {len(combined_audio)} bytes")
                        await websocket.send(json.dumps({
                            "type": "audio_stream",
                            "data": base64.b64encode(combined_audio).decode(),
                            "stream": True
                        }))
                    
                    # Check if more audio is coming
                    await asyncio.sleep(0.1)  # Small delay for buffering
                    
                    # Stop streaming if no more audio
                    if not conn['audio_buffer']:
                        conn['is_streaming'] = False
                        await websocket.send(json.dumps({
                            "type": "audio_end",
                            "stream": False
                        }))
                else:
                    await asyncio.sleep(0.05)  # Wait for audio
                    
        except Exception as e:
            logger.error(f"Error streaming audio for {client_id}: {e}")
    
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
    """Start the conversational Gemini Live API server"""
    server = ConversationalGeminiServer()
    
    logger.info("Starting Conversational Gemini 2.5 Flash Live API Server")
    logger.info("Server running on ws://localhost:8765")
    logger.info("Real conversational mode with smooth audio streaming")
    
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
            logger.info("Conversational WebSocket server is running...")
            await asyncio.Future()  # Run forever
            
    except Exception as e:
        logger.error(f"Failed to start conversational server: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())