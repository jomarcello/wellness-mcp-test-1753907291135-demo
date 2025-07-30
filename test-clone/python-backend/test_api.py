#!/usr/bin/env python3
"""
Test API key and model availability
"""
import os
from google import genai

# API Configuration
os.environ["GOOGLE_API_KEY"] = "AIzaSyB82katqt-X1myT_8Ig5IMFgfABLmNrclY"

def test_api():
    try:
        client = genai.Client()
        print("✅ Client created successfully")
        
        # Test models
        models = client.models.list()
        print(f"✅ Available models: {len(models)}")
        
        # Look for our model
        target_model = "gemini-2.5-flash-preview-native-audio-dialog"
        found = False
        
        for model in models:
            if target_model in model.name:
                print(f"✅ Found target model: {model.name}")
                found = True
                break
                
        if not found:
            print(f"❌ Model '{target_model}' not found")
            print("Available models:")
            for model in models:
                print(f"  - {model.name}")
                
    except Exception as e:
        print(f"❌ API test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api()