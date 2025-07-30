#!/usr/bin/env python3
"""
Simple Conversational Voice Agent - Text First
"""
import os
import asyncio
import json
import logging
import websockets
from google import genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration
os.environ["GEMINI_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

# Simple configuration - text first
MODEL = "gemini-2.5-flash-preview-native-audio-dialog"
CONFIG = {
    "response_modalities": ["TEXT"],
    "system_instruction": "คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic คลินิกความงาม ตอบเป็นภาษาไทยเท่านั้น"
}

class SimpleVoiceAgent:
    def __init__(self):
        self.client = genai.Client(
            http_options={"api_version": "v1beta"},
            api_key=os.environ.get("GEMINI_API_KEY")
        )
        
    async def handle_connection(self, websocket, path):
        """Handle WebSocket connection"""
        logger.info("Client connected")
        
        try:
            async with self.client.aio.live.connect(model=MODEL, config=CONFIG) as session:
                logger.info("Connected to Gemini Live API")
                
                # Send greeting
                await session.send(input="สวัสดีค่ะ ยินดีต้อนรับสู่ BeautyMed Clinic", end_of_turn=True)
                
                # Handle messages
                await asyncio.gather(
                    self.handle_frontend_messages(websocket, session),
                    self.handle_gemini_responses(websocket, session)
                )
                
        except Exception as e:
            logger.error(f"Error: {e}")
            await websocket.send(json.dumps({"type": "error", "message": str(e)}))

    async def handle_frontend_messages(self, websocket, session):
        """Handle messages from frontend"""
        try:
            async for message in websocket:
                data = json.loads(message)
                logger.info(f"Received: {data}")
                
                if data.get("type") == "text":
                    await session.send(input=data["text"], end_of_turn=True)
                    
        except Exception as e:
            logger.error(f"Frontend message error: {e}")

    async def handle_gemini_responses(self, websocket, session):
        """Handle responses from Gemini"""
        try:
            async for response in session.receive():
                if response.text is not None:
                    logger.info(f"Gemini response: {response.text}")
                    await websocket.send(json.dumps({
                        "type": "text",
                        "text": response.text
                    }))
                    
        except Exception as e:
            logger.error(f"Gemini response error: {e}")

async def main():
    agent = SimpleVoiceAgent()
    
    async with websockets.serve(agent.handle_connection, "localhost", 8765):
        logger.info("Simple voice agent started on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())