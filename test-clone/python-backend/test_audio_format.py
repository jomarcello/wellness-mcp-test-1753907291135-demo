#!/usr/bin/env python3
"""
Test different audio formats and voices for Thai
"""
import os
import asyncio
import logging
import base64
from google import genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set API key
os.environ["GEMINI_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

async def test_audio_formats():
    """Test different voice configurations"""
    
    client = genai.Client(
        http_options={"api_version": "v1beta"},
        api_key=os.environ.get("GEMINI_API_KEY")
    )
    
    # Test different configurations
    configs = [
        {
            "name": "Default (no voice config)",
            "config": {
                "response_modalities": ["AUDIO"],
                "system_instruction": "คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic ตอบเป็นภาษาไทยเท่านั้น"
            }
        },
        {
            "name": "Aoede voice",
            "config": {
                "response_modalities": ["AUDIO"],
                "system_instruction": "คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic ตอบเป็นภาษาไทยเท่านั้น",
                "speech_config": {
                    "voice_config": {
                        "prebuilt_voice_config": {
                            "voice_name": "Aoede"
                        }
                    }
                }
            }
        },
        {
            "name": "Puck voice",
            "config": {
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
        }
    ]
    
    for test_config in configs:
        logger.info(f"Testing: {test_config['name']}")
        
        try:
            async with client.aio.live.connect(
                model="models/gemini-2.0-flash-live-001",
                config=test_config['config']
            ) as session:
                
                # Send test message
                await session.send(input="สวัสดีค่ะ", end_of_turn=True)
                
                # Receive response
                response_count = 0
                async for response in session.receive():
                    response_count += 1
                    
                    if response.data is not None:
                        logger.info(f"✅ {test_config['name']}: Received {len(response.data)} bytes of audio")
                        
                        # Save first few bytes for inspection
                        if len(response.data) > 10:
                            first_bytes = response.data[:10]
                            logger.info(f"First 10 bytes: {[hex(b) for b in first_bytes]}")
                        
                    if response.text is not None:
                        logger.info(f"✅ {test_config['name']}: Text: {response.text}")
                    
                    # Stop after a few responses
                    if response_count >= 3:
                        break
                        
        except Exception as e:
            logger.error(f"❌ {test_config['name']}: Failed - {e}")
            
        logger.info("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_audio_formats())