const testThaiVoice = async () => {
  try {
    console.log('🧪 Testing Thai TTS API...');
    
    const response = await fetch('http://localhost:3002/api/thai-tts', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json' 
      },
      body: JSON.stringify({ 
        text: "สวัสดีค่ะ ยินดีต้อนรับสู่ BeautyMed Clinic ค่ะ ดิฉันชื่อ Robin ผู้ช่วยนัดหมาย",
        voice: "th-TH-Neural2-C"
      })
    });
    
    console.log('📡 Response status:', response.status);
    console.log('📡 Response headers:', [...response.headers.entries()]);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('❌ Thai TTS test failed:', response.status, errorText);
      return;
    }
    
    const data = await response.json();
    console.log('✅ Thai TTS test successful!');
    console.log('🔊 Audio data length:', data.audio ? data.audio.length : 'No audio data');
    console.log('🎵 MIME type:', data.mimeType);
    
    if (data.audio) {
      console.log('✅ Audio generated successfully!');
    } else {
      console.log('⚠️ No audio data received');
    }
    
  } catch (error) {
    console.error('❌ Test error:', error.message);
  }
};

// Test Thai STT as well
const testThaiSTT = async () => {
  try {
    console.log('🧪 Testing Thai STT API...');
    
    // This would need actual audio data in production
    const dummyAudioBase64 = "dummy_audio_data";
    
    const response = await fetch('http://localhost:3002/api/thai-stt', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json' 
      },
      body: JSON.stringify({ 
        audio: dummyAudioBase64
      })
    });
    
    console.log('📡 STT Response status:', response.status);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.log('⚠️ Thai STT test (expected to fail with dummy data):', response.status, errorText);
      return;
    }
    
    const data = await response.json();
    console.log('✅ Thai STT API responded:', data);
    
  } catch (error) {
    console.error('❌ STT Test error:', error.message);
  }
};

// Run tests
console.log('🚀 Starting Thai Voice API tests...');
console.log('🔧 Make sure the server is running on port 3002');
console.log('💡 Start server with: PRACTICE_ID=beautymed PORT=3002 npm run dev');
console.log('');

testThaiVoice().then(() => {
  console.log('');
  return testThaiSTT();
}).then(() => {
  console.log('');
  console.log('🏁 Tests completed!');
});