# Conversational Thai TTS Setup Guide

This guide explains how to make Google TTS voice conversations more natural and human-like for Thai language interactions.

## Overview

The conversational Thai TTS system enhances the basic Google Text-to-Speech API with:
- **Natural speech patterns** using SSML (Speech Synthesis Markup Language)
- **Context-aware responses** that adapt to conversation flow
- **Personalized interactions** using customer data
- **Multiple voice styles** (conversational, friendly, professional)
- **Fallback mechanisms** for development/testing

## Architecture

```
┌─────────────────────────────────────────┐
│         ThaiConversationalTTS           │
│  (Enhanced Conversation Service)        │
├─────────────────────────────────────────┤
│  • Context-aware response generation    │
│  • SSML-enhanced speech synthesis       │
│  • Natural conversation flow            │
│  • Multi-style voice configuration      │
└─────────────────────────────────────────┘
           │
┌──────────┴──────────┐
│  /api/thai-tts-conversational  │
│  (Google TTS Integration)      │
└────────────────────────────────┘
           │
┌──────────┴──────────┐
│  Google Cloud TTS   │
│  (th-TH-Chirp3-HD-Aoede) │
└─────────────────────┘
```

## Key Features

### 1. Conversational SSML Enhancement
The system adds natural speech elements:
- **Pauses**: Natural breathing breaks between phrases
- **Emphasis**: Stress on important words
- **Intonation**: Question patterns for queries
- **Rhythm**: Natural speech flow for Thai language

### 2. Context-Aware Responses
- **Personalization**: Uses customer names
- **Service context**: References specific treatments
- **Appointment details**: Includes dates/times
- **Sentiment adaptation**: Adjusts tone based on mood

### 3. Voice Styles
- **Conversational**: Natural, everyday speech
- **Friendly**: Warm and welcoming
- **Professional**: Business-appropriate tone

## Setup Instructions

### 1. Google Cloud Configuration

Set up Google Cloud credentials:

```bash
# Set environment variables
export GOOGLE_CLOUD_PROJECT_ID="your-project-id"
export GOOGLE_CLOUD_ACCESS_TOKEN="$(gcloud auth print-access-token)"
```

### 2. API Endpoints

The system provides two main endpoints:

#### Basic TTS
```
POST /api/thai-tts
{
  "text": "สวัสดีค่ะ",
  "voice": "th-TH-Neural2-C"
}
```

#### Conversational TTS
```
POST /api/thai-tts-conversational
{
  "text": "สวัสดีค่ะ",
  "voice": "th-TH-Chirp3-HD-Aoede",
  "style": "conversational"
}
```

### 3. Usage Examples

#### Basic Usage
```typescript
import { thaiConversationalTTS } from '@/lib/thai-conversational-tts';

// Simple speech
await thaiConversationalTTS.speak('สวัสดีค่ะ', {
  voice: 'th-TH-Chirp3-HD-Aoede',
  style: 'conversational',
  speed: 0.9,
  pitch: 1,
  volume: 2
});
```

#### Context-Aware Usage
```typescript
const context = {
  customerName: 'สมชาย',
  service: 'โบท็อกซ์',
  appointmentDate: '15/07/2025',
  appointmentTime: '14:00',
  previousMessages: ['ขอบคุณค่ะ']
};

await thaiConversationalTTS.speak(
  'ยืนยันการนัดหมายนะคะ',
  thaiConversationalTTS.getVoiceConfig('robin-conversational'),
  context
);
```

### 4. SSML Features

The conversational TTS automatically adds:

#### Natural Pauses
```xml
<break time="200ms"/>ค่ะ<break time="100ms"/>
```

#### Question Intonation
```xml
<prosody pitch="+2st">ใช่ไหม</prosody><break time="300ms"/>
```

#### Emphasis
```xml
<emphasis level="moderate">ขอบคุณ</emphasis>
```

#### Numbers & Dates
```xml
<say-as interpret-as="cardinal">25</say-as>
<say-as interpret-as="date" format="dmY">15/07/2025</say-as>
```

## Voice Configuration

### Available Voices
- **th-TH-Chirp3-HD-Aoede**: High-definition Thai female voice
- **th-TH-Neural2-C**: Neural Thai female voice
- **th-TH-Standard-A**: Standard Thai female voice

### Voice Styles
```typescript
const voiceStyles = {
  'robin-conversational': {
    voice: 'th-TH-Chirp3-HD-Aoede',
    style: 'conversational',
    speed: 0.95,
    pitch: 1,
    volume: 2
  },
  'robin-friendly': {
    voice: 'th-TH-Chirp3-HD-Aoede',
    style: 'friendly',
    speed: 0.9,
    pitch: 1,
    volume: 2
  },
  'robin-professional': {
    voice: 'th-TH-Chirp3-HD-Aoede',
    style: 'professional',
    speed: 0.85,
    pitch: 0,
    volume: 1
  }
};
```

## Conversation Flow Examples

### 1. Greeting
**Input**: "สวัสดี"
**Enhanced**: "สวัสดีค่ะ ดิฉันชื่อ Robin ผู้ช่วยนัดหมายค่ะ วันนี้พอจะช่วยอะไรได้บ้างคะ?"

### 2. Service Inquiry
**Input**: "สนใจโบท็อกซ์"
**Enhanced**: "ดีมากค่ะ สำหรับโบท็อกซ์ คุณสะดวกวันไหนคะ?"

### 3. Appointment Confirmation
**Input**: "ยืนยันนัดหมาย"
**Enhanced**: "ขอยืนยันการนัดหมายนะคะ โบท็อกซ์ วันที่ 15/07/2025 เวลา 14:00 ใช่ไหมคะ?"

## Testing Commands

### Direct API Test
```bash
curl -X POST http://localhost:3000/api/thai-tts-conversational \
  -H "Content-Type: application/json" \
  -d '{
    "text": "สวัสดีค่ะ ยินดีต้อนรับสู่ BeautyMed Clinic",
    "voice": "th-TH-Chirp3-HD-Aoede",
    "style": "conversational"
  }'
```

### Browser Test
```typescript
// Test basic functionality
await thaiConversationalTTS.speak('สวัสดีค่ะ');

// Test with context
await thaiConversationalTTS.speak(
  'ขอบคุณค่ะคุณสมชาย',
  thaiConversationalTTS.getVoiceConfig('robin-friendly'),
  { customerName: 'สมชาย' }
);
```

## Fallback Mechanism

When Google Cloud credentials are not available, the system falls back to:
1. **Browser TTS**: Uses Web Speech API
2. **Mock responses**: Returns placeholder audio
3. **Console logging**: Shows what would be spoken

## Integration with Existing System

### Replace Basic TTS
```typescript
// Old way
import { speakThai } from '@/lib/thai-conversation';

// New way
import { thaiConversationalTTS } from '@/lib/thai-conversational-tts';
```

### Update Components
Replace `ThaiVoiceDemo` with `ThaiConversationalVoiceDemo` for enhanced functionality.

## Environment Variables

Create `.env.local`:
```bash
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_ACCESS_TOKEN=your-access-token
```

## Troubleshooting

### Common Issues

1. **No audio output**
   - Check browser permissions for microphone
   - Verify Google Cloud credentials
   - Check console for errors

2. **Thai voice not found**
   - Ensure Thai language pack is installed
   - Use fallback browser TTS

3. **SSML not working**
   - Verify Google Cloud TTS API is enabled
   - Check SSML syntax validity

### Debug Mode
Enable debug logging:
```typescript
console.log('SSML:', ssmlText);
console.log('Context:', conversationContext);
```

## Performance Optimization

- **Audio caching**: Cache generated audio for repeated phrases
- **Preloading**: Preload common responses
- **Streaming**: Use streaming for long conversations
- **Compression**: Optimize audio quality vs. size

## Security Considerations

- **Token rotation**: Regularly refresh Google Cloud access tokens
- **Rate limiting**: Implement API rate limiting
- **Input validation**: Sanitize user input before TTS processing
- **HTTPS only**: Ensure all API calls use HTTPS

## Future Enhancements

- **Voice cloning**: Custom voice training
- **Emotion detection**: Adapt tone based on sentiment
- **Multi-language**: Support for other languages
- **Real-time streaming**: Continuous conversation flow
- **Voice biometrics**: Speaker identification
