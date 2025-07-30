#!/usr/bin/env python3
"""
Fixed Conversational Voice Agent - WebSocket Compatible
"""
import os
import asyncio
import base64
import json
import logging
import websockets
from google import genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration
os.environ["GEMINI_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

# Official configuration
MODEL = "gemini-2.5-flash-preview-native-audio-dialog"
CONFIG = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic คลินิกความงาม ตอบเป็นภาษาไทยเท่านั้น"
}

class ConversationalVoiceAgent:
    def __init__(self):
        self.client = genai.Client(
            http_options={"api_version": "v1beta"},
            api_key=os.environ.get("GEMINI_API_KEY")
        )
        self.running = False
        
    async def handle_frontend_connection(self, websocket, path):
        """Handle WebSocket connection from frontend"""
        logger.info("Frontend connected")
        
        try:
            async with self.client.aio.live.connect(model=MODEL, config=CONFIG) as session:
                self.running = True
                
                # Send initial greeting
                await session.send(input="สวัสดีค่ะ ยินดีต้อนรับสู่ BeautyMed Clinic", end_of_turn=True)
                
                # Run concurrent tasks
                tasks = [
                    asyncio.create_task(self.handle_gemini_responses(session, websocket)),
                    asyncio.create_task(self.handle_frontend_messages(websocket, session))
                ]
                
                await asyncio.gather(*tasks)
                
        except Exception as e:
            logger.error(f"Connection error: {e}")
            try:
                await websocket.send(json.dumps({"type": "error", "message": str(e)}))
            except:
                pass
        finally:
            self.running = False
            logger.info("Frontend disconnected")

    async def handle_gemini_responses(self, session, websocket):
        """Handle responses from Gemini"""
        try:
            async for response in session.receive():
                if not self.running:
                    break
                    
                # Handle audio response
                if response.data is not None:
                    logger.info(f"Received audio data: {len(response.data)} bytes")
                    await websocket.send(json.dumps({
                        "type": "audio",
                        "data": base64.b64encode(response.data).decode()
                    }))
                
                # Handle text response
                if response.text is not None:
                    logger.info(f"Received text: {response.text}")
                    await websocket.send(json.dumps({
                        "type": "text",
                        "text": response.text
                    }))
                    
        except Exception as e:
            logger.error(f"Error handling Gemini responses: {e}")
            self.running = False

    async def handle_frontend_messages(self, websocket, session):
        """Handle messages from frontend"""
        try:
            async for message in websocket:
                if not self.running:
                    break
                    
                data = json.loads(message)
                
                if data.get("type") == "text":
                    await session.send(input=data["text"], end_of_turn=True)
                    
                elif data.get("type") == "audio_continuous":
                    # Handle continuous audio from frontend
                    try:
                        audio_data = base64.b64decode(data["data"])
                        await session.send_realtime_input(audio={"data": audio_data, "mime_type": "audio/pcm"})
                    except Exception as e:
                        logger.error(f"Error processing audio: {e}")
                        
                elif data.get("type") == "stop":
                    self.running = False
                    break
                    
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
    logger.info("Server will run on ws://localhost:8765")
    
    try:
        async with websockets.serve(
            agent.handle_frontend_connection, 
            "localhost", 
            8765,
            ping_interval=None,
            ping_timeout=None
        ):
            logger.info("Conversational voice agent started on ws://localhost:8765")
            await asyncio.Future()  # Run forever
            
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())