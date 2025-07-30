# 🎤 CREATE ECHTE VOICE AGENT - STAP VOOR STAP

## PROBLEEM
De voice agent gebruikt fake responses - we willen een **echte conversational AI** die:
- 🎤 Speech-to-speech conversation (geen tekst tussenin)  
- 🤖 Echte AI die begrijpt en reageert
- 🇹🇭 Thai voice support
- 📞 Real-time voice interaction

## OPLOSSING: ElevenLabs Conversational AI

### STAP 1: ElevenLabs Account + API Key
1. Ga naar https://elevenlabs.io
2. Maak account aan (gratis tier beschikbaar)
3. Ga naar Settings → API Keys
4. Kopieer je API key
5. Voeg toe aan `.env.local`:
```
ELEVENLABS_API_KEY=sk_jouw_api_key_hier
```

### STAP 2: Maak Thai Voice Agent in ElevenLabs
1. Log in op ElevenLabs dashboard
2. Ga naar "Conversational AI" → "Agents"  
3. Klik "Create New Agent"
4. Configureer:
   - **Name**: BeautyMed Thai Assistant
   - **Voice**: Kies een Thai voice (of trainable voice)
   - **Language**: Thai (th-TH)
   - **Prompt**: 
   ```
   คุณคือ Robin ผู้ช่วยนัดหมายของ BeautyMed Clinic 
   ร่วมกับ Dr. Siriporn Thanakit 
   
   บริการ: โบท็อกซ์, ฟิลเลอร์, ดูแลผิวหน้า, รักษาสิว, ขจัดขน
   
   เป้าหมาย:
   - ช่วยลูกค้านัดหมาย
   - ตอบคำถามเรื่องบริการ  
   - พูดแบบเป็นมิตรและสุภาพ
   - ให้เวลานัดหมายที่เป็นจริง
   ```
5. **SAVE** en kopieer de **Agent ID**

### STAP 3: Update Practice Config
Vervang in `/src/lib/practice-config.ts`:
```typescript
agentId: 'agent_ECHTE_ELEVENLABS_ID_HIER',
```

### STAP 4: Test Real Voice Agent
1. Restart development server: `npm run dev`
2. Ga naar BeautyMed demo (port 3002)
3. Klik "Start Call" 
4. **SPREEK THAI** - de agent moet nu echt antwoorden!

## WAAROM DIT WERKT
- **ElevenLabs Conversational AI** = speech-to-speech
- **Geen mock responses** meer
- **Echte AI conversation** met context
- **Thai voice support** native

## ALTERNATIEF: OpenAI Realtime API
Als ElevenLabs geen Thai heeft:
1. Gebruik OpenAI Realtime API (GPT-4 Audio)
2. Combineer met ElevenLabs TTS voor Thai voice
3. Implementeer in nieuwe `/api/realtime-voice` route

## CHECKLIST
- [ ] ElevenLabs account aangemaakt
- [ ] API key toegevoegd aan .env.local
- [ ] Thai voice agent gemaakt in dashboard
- [ ] Agent ID geupdate in config
- [ ] Server gerestart
- [ ] Voice agent getest
- [ ] Thai conversation werkt!

## SUPPORT
Als je problemen hebt:
1. Check ElevenLabs dashboard voor agent status
2. Check browser console voor errors
3. Verify API key in .env.local
4. Test eerst met English agent