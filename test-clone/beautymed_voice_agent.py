# -*- coding: utf-8 -*-
"""
BeautyMed Clinic Voice Assistant
Real-time voice conversation with Gemini Live API for BeautyMed clinic appointments
"""

import os
import base64
import json
import numpy as np
import gradio as gr
import websockets.sync.client
from gradio_webrtc import StreamHandler, WebRTC

# Configuration
class BeautyMedConfig:
    """Configuration for BeautyMed voice assistant with Play.ht Thai voice."""
    def __init__(self):
        self.api_key = "9a1ffef880fd4dab94c34d49267812b3"
        self.agent_id = "thai-lady-J0JZKhhZhpgpwebqoE3zQ"
        self.host = "api.play.ht"
        self.ws_url = f"wss://{self.host}/v2/live?api_key={self.api_key}&agent_id={self.agent_id}"

class AudioProcessor:
    """Handles encoding and decoding of audio data for Play.ht."""
    @staticmethod
    def encode_audio(data, sample_rate):
        """Encodes audio data to base64 for Play.ht."""
        encoded = base64.b64encode(data.tobytes()).decode("UTF-8")
        return {
            "type": "audio_stream",
            "audio_data": encoded,
            "format": "pcm",
            "sample_rate": sample_rate
        }

    @staticmethod
    def process_audio_response(data):
        """Decodes audio data from base64."""
        audio_data = base64.b64decode(data)
        return np.frombuffer(audio_data, dtype=np.int16)

# BeautyMed Gemini Handler
class BeautyMedHandler(StreamHandler):
    """Handles WebSocket communication with Gemini API for BeautyMed."""
    def __init__(self):
        super().__init__()
        self.config = BeautyMedConfig()
        self.processor = AudioProcessor()
        self.ws = None
        self.setup_instructions = {
            "type": "setup",
            "config": {
                "voice": {
                    "agent_id": self.config.agent_id,
                    "language": "th",
                    "voice_style": "professional"
                },
                "system_prompt": """คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic คลินิกความงาม 

ตอบเป็นภาษาไทยเท่านั้น โดยใช้คำพูดที่สุภาพและเป็นมิตร

หน้าที่ของคุณ:
1. ต้อนรับผู้ป่วยด้วยความอบอุ่น
2. ช่วยจองนัดหมายสำหรับบริการต่างๆ ของคลินิก
3. แนะนำบริการความงามของคลินิก
4. ตอบคำถามเกี่ยวกับการดูแลก่อนและหลังการรักษา
5. สอบถามข้อมูลที่จำเป็นสำหรับการนัดหมาย

บริการของคลินิก:
- ฉีดโบท็อกซ์: 3,000-8,000 บาท
- ฟิลเลอร์: 8,000-15,000 บาท  
- การรักษาสิว: 2,000-5,000 บาท
- เลเซอร์กำจัดขน: 1,500-5,000 บาท
- ฟอโตเฟเชียล: 2,500-4,000 บาท
- การดูแลผิวหน้า: 1,000-3,000 บาท

เวลาทำการ: จันทร์-เสาร์ 9:00-18:00
โทรศัพท์: 02-xxx-xxxx

ให้คำตอบสั้นๆ กระชับ และช่วยเหลือผู้ป่วยอย่างเต็มที่"""
            }
        }
    
    def copy(self):
        """Return a copy of this handler."""
        return BeautyMedHandler()
    
    def emit(self, *args, **kwargs):
        """Emit method for StreamHandler compatibility."""
        pass

    def send_initial_setup(self):
        """Send the initial setup to configure BeautyMed assistant with Play.ht."""
        if self.ws:
            self.ws.send(json.dumps(self.setup_instructions))
            print("✅ BeautyMed Thai assistant configured with Play.ht")

    def receive(self, frame: tuple[int, np.ndarray]):
        """Process incoming audio frame and send to Play.ht."""
        sample_rate, data = frame
        try:
            if self.ws is None:
                print("🔌 Connecting to Play.ht Thai Voice API...")
                self.ws = websockets.sync.client.connect(self.config.ws_url)
                self.send_initial_setup()
                print("✅ Connected and configured for BeautyMed with Thai voice")

            # Encode and send audio
            audio_msg = self.processor.encode_audio(data, sample_rate)
            self.ws.send(json.dumps(audio_msg))

            # Receive and process response
            for message in self.ws:
                response = json.loads(message)
                
                # Log for debugging
                if response.get("type") == "text" and response.get("text"):
                    print(f"🗣️  Thai Robin: {response['text']}")
                
                # Process audio response from Play.ht
                if response.get("type") == "audio" and response.get("audio_data"):
                    audio_data = self.processor.process_audio_response(response["audio_data"])
                    yield (24000, audio_data)

        except websockets.exceptions.ConnectionClosed:
            print("🔌 Connection closed, reconnecting...")
            self.ws = None
        except Exception as e:
            print(f"❌ Error: {e}")
            self.ws = None

def create_beautymed_interface():
    """Create the BeautyMed voice interface."""
    with gr.Blocks(
        title="🏥 BeautyMed Clinic - Voice Assistant",
        css="""
        .gradio-container {
            background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .gr-button {
            background: linear-gradient(135deg, #e17055 0%, #d63031 100%);
            border: none;
            color: white;
            font-weight: bold;
        }
        .gr-button:hover {
            background: linear-gradient(135deg, #d63031 0%, #c0392b 100%);
        }
        """
    ) as demo:
        
        with gr.Row():
            gr.HTML("""
                <div style="text-align: center; padding: 20px;">
                    <h1 style="color: #e17055; margin-bottom: 10px;">💄 BeautyMed Clinic</h1>
                    <h2 style="color: #2d3436; margin-bottom: 10px;">Thai Voice Assistant - Robin</h2>
                    <p style="color: #636e72; font-size: 16px;">พูดคุยกับ Robin ผู้ช่วยนัดหมายด้วยเสียงภาษาไทย</p>
                    <p style="color: #636e72; font-size: 14px;">🎤 กดปุ่ม Record แล้วพูดเลย Robin จะตอบด้วยเสียงไทย</p>
                </div>
            """)
        
        with gr.Row():
            with gr.Column():
                webrtc = WebRTC(
                    label="🎙️ Voice Chat with Thai Robin",
                    modality="audio",
                    mode="send-receive",
                )
                
                gr.HTML("""
                    <div style="background: rgba(255,255,255,0.9); padding: 15px; border-radius: 10px; margin-top: 15px;">
                        <h3 style="color: #e17055; margin-bottom: 10px;">📋 BeautyMed Services:</h3>
                        <ul style="color: #2d3436; line-height: 1.6;">
                            <li>💉 ฉีดโบท็อกซ์: 3,000-8,000 บาท</li>
                            <li>💋 ฟิลเลอร์: 8,000-15,000 บาท</li>
                            <li>✨ การรักษาสิว: 2,000-5,000 บาท</li>
                            <li>🔥 เลเซอร์กำจัดขน: 1,500-5,000 บาท</li>
                            <li>🌟 ฟอโตเฟเชียล: 2,500-4,000 บาท</li>
                            <li>🧴 การดูแลผิวหน้า: 1,000-3,000 บาท</li>
                        </ul>
                        <p style="color: #00b894; font-weight: bold; margin-top: 10px;">
                            🕒 เวลาทำการ: จันทร์-เสาร์ 9:00-18:00
                        </p>
                    </div>
                """)

        # Set up the handler
        webrtc.stream(BeautyMedHandler().receive, inputs=[webrtc], outputs=[webrtc])
        
        with gr.Row():
            gr.HTML("""
                <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.8); border-radius: 10px; margin-top: 10px;">
                    <p style="color: #636e72; font-size: 12px;">
                        💡 Tips: พูดชัดๆ ใกล้ไมค์ • Robin จะตอบเป็นภาษาไทยด้วยเสียงผู้หญิง • หากไม่ได้ยินให้ลองปรับเสียง
                    </p>
                </div>
            """)

    return demo

if __name__ == "__main__":
    print("🏥 Starting BeautyMed Thai Voice Assistant...")
    print("🎤 Thai Robin is ready to help with appointments!")
    print("🌐 Open http://localhost:7860 in your browser")
    print("📱 Click 'Record' and start talking in Thai!")
    
    demo = create_beautymed_interface()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_api=False
    )