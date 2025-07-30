"""
Gemini Live API Server for Thai Beauty Clinic Voice Assistant
Real-time audio dialog with Zephyr voice
"""

import os
import asyncio
import base64
import io
import json
import traceback
import websockets
import logging

from google import genai
from google.genai import types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set your API key
os.environ["GEMINI_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

client = genai.Client(
    http_options={"api_version": "v1beta"},
    api_key=os.environ.get("GEMINI_API_KEY")
)

# Thai Beauty Clinic configuration
THAI_SYSTEM_PROMPT = """
คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic คลินิกความงาม
ดูแลโดย Dr. Siriporn Thanakit ซึ่งเชี่ยวชาญด้านความงาม

บริการที่มี:
- โบท็อกซ์ (Botox) - ลดริ้วรอยและปรับรูปหน้า
- ฟิลเลอร์ (Filler) - เติมร่องลึกและเสริมรูปหน้า
- รักษาสิว (Acne Treatment) - ทำความสะอาดและรักษาสิว
- ขจัดขน (Hair Removal) - เลเซอร์ขจัดขน
- มาส์กหน้า (Facial Mask) - ดูแลผิวหน้า
- ทำผิวขาว (Skin Whitening) - ปรับสีผิว
- ดูแลผิวหน้า (Facial Care) - ความสะอาดผิวลึก

คำแนะนำสำคัญ:
- ตอบเป็นภาษาไทยเท่านั้น ห้ามใช้ภาษาอื่น
- พูดแบบเป็นกันเองและอบอุ่น
- ถามข้อมูลที่จำเป็นเพื่อนัดหมาย (ชื่อ, เบอร์, บริการ, วันเวลา)
- ให้ข้อมูลเกี่ยวกับบริการเมื่อถูกถาม
- ตอบสั้นๆ กะทัดรัด 1-2 ประโยค
- เป็นมิตรและให้ความช่วยเหลือ

เริ่มต้นด้วยการทักทายและแนะนำตัวเป็นภาษาไทย
"""

CONFIG = {
    "response_modalities": ["AUDIO"],
    "system_instruction": THAI_SYSTEM_PROMPT,
}

class GeminiLiveServer:
    def __init__(self):
        self.websocket = None
        self.session = None

    async def handle_websocket(self, websocket, path):
        """Handle WebSocket connections from the frontend"""
        logger.info(f"New WebSocket connection from {websocket.remote_address}")
        self.websocket = websocket
        
        try:
            # Connect to Gemini Live API
            logger.info("Connecting to Gemini Live API...")
            async with client.aio.live.connect(model="models/gemini-2.0-flash-live-001", config=CONFIG) as session:
                self.session = session
                logger.info("Connected to Gemini Live API successfully")
                
                # Start background tasks
                task1 = asyncio.create_task(self.handle_frontend_messages())
                task2 = asyncio.create_task(self.handle_gemini_messages())
                
                # Send initial greeting
                await session.send(input="สวัสดีค่ะ ยินดีต้อนรับสู่ BeautyMed Clinic", end_of_turn=True)
                
                # Wait for both tasks
                await asyncio.gather(task1, task2)

        except Exception as e:
            logger.error(f"Error in websocket handler: {e}")
            traceback.print_exc()
            # Send error to frontend
            if self.websocket:
                await self.websocket.send(json.dumps({
                    "type": "error",
                    "message": str(e)
                }))
        finally:
            logger.info("WebSocket connection closed")

    async def handle_frontend_messages(self):
        """Handle messages from the frontend WebSocket"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                logger.info(f"Received message from frontend: {data.get('type')}")
                
                if data.get("type") == "audio":
                    # Receive audio data from frontend
                    audio_data = base64.b64decode(data["data"])
                    await self.session.send(input=audio_data)
                
                elif data.get("type") == "text":
                    # Receive text message from frontend
                    text = data.get("text", "")
                    await self.session.send(input=text, end_of_turn=True)
                
                elif data.get("type") == "start_conversation":
                    # Start a new conversation
                    await self.session.send(input="เริ่มการสนทนาใหม่", end_of_turn=True)

        except websockets.exceptions.ConnectionClosed:
            logger.info("Frontend disconnected")
        except Exception as e:
            logger.error(f"Error handling frontend messages: {e}")

    async def handle_gemini_messages(self):
        """Handle messages from Gemini Live API"""
        try:
            async for response in self.session.receive():
                logger.info(f"Received response from Gemini: {type(response)}")
                
                # Handle audio data
                if response.data is not None:
                    logger.info("Sending audio response to frontend")
                    await self.websocket.send(json.dumps({
                        "type": "audio",
                        "data": base64.b64encode(response.data).decode()
                    }))
                
                # Handle text response
                if response.text is not None:
                    logger.info(f"Gemini text: {response.text}")
                    await self.websocket.send(json.dumps({
                        "type": "text",
                        "text": response.text
                    }))

        except Exception as e:
            logger.error(f"Error handling Gemini messages: {e}")
            traceback.print_exc()

async def main():
    """Start the WebSocket server"""
    server = GeminiLiveServer()
    
    logger.info("Starting Gemini Live API Server on ws://localhost:8765")
    logger.info("Thai Beauty Clinic Voice Assistant ready!")
    logger.info("Make sure to have the API key set and dependencies installed")
    
    try:
        async with websockets.serve(server.handle_websocket, "localhost", 8765):
            logger.info("WebSocket server is running...")
            await asyncio.Future()  # Run forever
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())