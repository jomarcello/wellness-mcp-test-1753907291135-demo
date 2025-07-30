#!/usr/bin/env python3
"""
Test script to verify Gemini Live API connection and Thai voice
"""
import os
import asyncio
import logging
from google import genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set API key
os.environ["GEMINI_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

async def test_gemini_connection():
    """Test connection to Gemini Live API"""
    try:
        # Create client
        client = genai.Client(
            http_options={"api_version": "v1beta"},
            api_key=os.environ.get("GEMINI_API_KEY")
        )
        
        # Test configuration
        config = {
            "response_modalities": ["AUDIO"],
            "system_instruction": "คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic ตอบเป็นภาษาไทยเท่านั้น",
            "speech_config": {
                "voice_config": {
                    "prebuilt_voice_config": {
                        "voice_name": "Puck"
                    }
                }
            }
        }
        
        logger.info("Testing Gemini Live API connection...")
        
        # Connect to Gemini Live API
        async with client.aio.live.connect(
            model="models/gemini-2.0-flash-live-001",
            config=config
        ) as session:
            logger.info("✅ Connected to Gemini Live API successfully!")
            
            # Test text input
            await session.send(input="สวัสดีค่ะ", end_of_turn=True)
            logger.info("✅ Sent test message")
            
            # Receive response
            response_count = 0
            async for response in session.receive():
                response_count += 1
                
                if response.data is not None:
                    logger.info(f"✅ Received audio response: {len(response.data)} bytes")
                    
                if response.text is not None:
                    logger.info(f"✅ Received text response: {response.text}")
                
                # Stop after first response
                if response_count >= 3:
                    break
                    
        logger.info("✅ Test completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gemini_connection())