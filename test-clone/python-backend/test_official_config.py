#!/usr/bin/env python3
"""
Test the official Gemini 2.5 Flash configuration
"""
import os
import asyncio
import logging
from google import genai
from google.genai import types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set API key
os.environ["GEMINI_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

async def test_official_config():
    """Test the official configuration"""
    
    client = genai.Client(
        http_options={"api_version": "v1beta"},
        api_key=os.environ.get("GEMINI_API_KEY")
    )
    
    # Official configuration
    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        media_resolution="MEDIA_RESOLUTION_MEDIUM",
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Zephyr")
            )
        ),
        system_instruction="คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic ตอบเป็นภาษาไทยเท่านั้น",
        context_window_compression=types.ContextWindowCompressionConfig(
            trigger_tokens=25600,
            sliding_window=types.SlidingWindow(target_tokens=12800),
        ),
    )
    
    logger.info("Testing official Gemini 2.5 Flash configuration...")
    
    try:
        async with client.aio.live.connect(
            model="models/gemini-2.5-flash-preview-native-audio-dialog",
            config=config
        ) as session:
            
            logger.info("✅ Connected to Gemini 2.5 Flash Live API successfully!")
            
            # Test with original send method (seems to be correct)
            await session.send(
                input="สวัสดีค่ะ",
                end_of_turn=True
            )
            logger.info("✅ Sent test message using official method")
            
            # Receive response using official pattern
            turn = session.receive()
            response_count = 0
            async for response in turn:
                response_count += 1
                
                if response.data is not None:
                    logger.info(f"✅ Received high-quality audio: {len(response.data)} bytes")
                    
                if response.text is not None:
                    logger.info(f"✅ Received text: {response.text}")
                
                # Stop after first complete response
                if response_count >= 3:
                    break
                    
            logger.info("✅ Official configuration test completed successfully!")
            
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_official_config())