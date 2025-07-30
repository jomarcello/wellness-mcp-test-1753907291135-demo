#!/usr/bin/env python3
"""
Test script to check audio setup
"""
import pyaudio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_audio_setup():
    """Test audio input/output setup"""
    try:
        pya = pyaudio.PyAudio()
        
        # Test input
        print("Testing audio input...")
        input_info = pya.get_default_input_device_info()
        print(f"Default input device: {input_info['name']}")
        print(f"Max input channels: {input_info['maxInputChannels']}")
        
        # Test output
        print("\nTesting audio output...")
        output_info = pya.get_default_output_device_info()
        print(f"Default output device: {output_info['name']}")
        print(f"Max output channels: {output_info['maxOutputChannels']}")
        
        # Test stream creation
        print("\nTesting stream creation...")
        input_stream = pya.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        
        output_stream = pya.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=24000,
            output=True
        )
        
        print("✅ Audio streams created successfully!")
        
        input_stream.close()
        output_stream.close()
        pya.terminate()
        
        print("✅ Audio setup test completed successfully!")
        
    except Exception as e:
        print(f"❌ Audio test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_audio_setup()