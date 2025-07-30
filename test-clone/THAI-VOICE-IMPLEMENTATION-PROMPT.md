# Thai Voice Agent Implementation Prompt

## Objective
Add Thai language support to voice agent using Google Cloud TTS instead of ElevenLabs.

## Key Requirements
1. Replace ElevenLabs with Google TTS for Thai voices
2. Enable conversational Thai speech
3. Target Thai businesses (beauty/medical/wellness)

## Implementation Steps

### 1. Google TTS Setup
```bash
# Enable APIs
gcloud services enable texttospeech.googleapis.com speech.googleapis.com

# Install dependencies
npm install @google-cloud/text-to-speech @google-cloud/speech
```

### 2. Create Thai TTS API Route
Create `src/app/api/thai-tts/route.ts`:
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { TextToSpeechClient } from '@google-cloud/text-to-speech';

const client = new TextToSpeechClient();

export async function POST(request: NextRequest) {
  const { text, voice = 'th-TH-Chirp3-HD-Aoede' } = await request.json();
  
  const [response] = await client.synthesizeSpeech({
    input: { text },
    voice: { 
      languageCode: 'th-TH', 
      name: voice,
      ssmlGender: 'FEMALE'
    },
    audioConfig: { 
      audioEncoding: 'MP3',
      speakingRate: 0.9
    },
  });
  
  return NextResponse.json({ 
    audio: response.audioContent.toString('base64'),
    mimeType: 'audio/mp3'
  });
}
```

### 3. Thai Speech-to-Text Route
Create `src/app/api/thai-stt/route.ts`:
```typescript
import { SpeechClient } from '@google-cloud/speech';

const client = new SpeechClient();

export async function POST(request: NextRequest) {
  const { audio } = await request.json();
  
  const [response] = await client.recognize({
    audio: { content: audio },
    config: {
      encoding: 'MP3',
      sampleRateHertz: 16000,
      languageCode: 'th-TH',
    },
  });
  
  return NextResponse.json({ 
    text: response.results?.[0]?.alternatives?.[0]?.transcript || '' 
  });
}
```

### 4. Thai Conversation Handler
Create `src/lib/thai-conversation.ts`:
```typescript
export const thaiResponses = {
  greeting: "สวัสดีค่ะ ดิฉันชื่อ Robin ผู้ช่วยนัดหมายค่ะ วันนี้พอจะช่วยอะไรได้บ้างคะ?",
  askDate: "คุณสะดวกวันไหนคะ?",
  askTime: "เวลาไหนคะ?",
  confirm: "ขอยืนยันการนัดหมายนะคะ วันที่ {date} เวลา {time} ใช่ไหมคะ?"
};

export function getThaiResponse(intent: string, context: any) {
  return thaiResponses[intent as keyof typeof thaiResponses] || thaiResponses.greeting;
}
```

### 5. Update Voice Demo Component
Update `src/components/VoiceDemo.tsx`:
```typescript
// Add Thai voice option
const thaiVoices = [
  { id: 'th-TH-Chirp3-HD-Aoede', name: 'Thai Female - Aoede' },
  { id: 'th-TH-Chirp3-HD-Demeter', name: 'Thai Female - Demeter' },
  { id: 'th-TH-Chirp3-HD-Puck', name: 'Thai Male - Puck' }
];

// Add Thai language toggle
const [language, setLanguage] = useState<'en' | 'th'>('th');

// Update TTS calls to use Thai endpoints
const speakThai = async (text: string) => {
  const response = await fetch('/api/thai-tts', {
    method: 'POST',
    body: JSON.stringify({ text })
  });
  const { audio } = await response.json();
  playAudio(audio);
};
```

### 6. Environment Variables
Add to `.env.local`:
```
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
GOOGLE_CLOUD_PROJECT=your-project-id
```

### 7. Quick Test Script
Create `scripts/test-thai-voice.js`:
```javascript
const testThaiVoice = async () => {
  const response = await fetch('http://localhost:3000/api/thai-tts', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      text: "สวัสดีค่ะ ยินดีต้อนรับสู่ BeautyMed ค่ะ" 
    })
  });
  
  const data = await response.json();
  console.log('Thai TTS test:', data.audio ? 'Success' : 'Failed');
};

testThaiVoice();
```

## Testing Commands
```bash
# Start development server
npm run dev

# Test Thai TTS
node scripts/test-thai-voice.js

# Test with curl
curl -X POST http://localhost:3000/api/thai-tts \
  -H "Content-Type: application/json" \
  -d '{"text":"สวัสดีค่ะ"}'
```

## Thai Business Keywords for Lead Scraping
Add to lead scraper:
```javascript
const thaiKeywords = [
  'คลินิกความงาม', 'สปา', 'นวด', 'ทันตกรรม', 
  'ความงาม', 'ผิวพรรณ', 'ลดน้ำหนัก'
];
```

## Next Actions
1. Set up Google Cloud service account
2. Run test script to verify Thai TTS
3. Update voice demo with Thai toggle
4. Test conversation flow in Thai
