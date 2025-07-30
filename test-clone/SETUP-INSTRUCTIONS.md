# 🚨 CORS Error Fix - Setup Instructions

## Het probleem
Je krijgt een "Vapi error (cors): Unknown error" omdat de VAPI API keys niet zijn geconfigureerd.

## ✅ Oplossing

### Stap 1: Maak een .env.local bestand
Maak een nieuw bestand genaamd `.env.local` in de `agents-demo` directory met de volgende inhoud:

```bash
# VAPI Configuration
# Get your API keys from https://dashboard.vapi.ai
NEXT_PUBLIC_VAPI_PUBLIC_KEY=your_vapi_public_key_here
VAPI_PRIVATE_KEY=your_vapi_private_key_here

# ElevenLabs Configuration (optional)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# OpenAI Configuration (optional)
OPENAI_API_KEY=your_openai_api_key_here

# Nari Dia TTS Configuration
NARI_DIA_SERVER_URL=http://localhost:7860
```

### Stap 2: Verkrijg je VAPI API keys
1. Ga naar [https://dashboard.vapi.ai](https://dashboard.vapi.ai)
2. Maak een account aan of log in
3. Ga naar de API Keys sectie
4. Kopieer je **Public Key** en **Private Key**
5. Vervang `your_vapi_public_key_here` en `your_vapi_private_key_here` in het `.env.local` bestand

### Stap 3: Herstart de Next.js server
```bash
# Stop de huidige server (Ctrl+C)
# Start opnieuw
npm run dev
```

### Stap 4: Test de applicatie
1. Ga naar [http://localhost:3000](http://localhost:3000)
2. De Nari Dia TTS server status zou nu "Server available" moeten tonen
3. Probeer een call te starten - de CORS error zou opgelost moeten zijn

## 🔧 Alternatieve oplossing (voor testen zonder VAPI account)

Als je geen VAPI account wilt maken, kun je de demo in "mock mode" gebruiken:

1. Vervang in het `.env.local` bestand:
```bash
NEXT_PUBLIC_VAPI_PUBLIC_KEY=demo_mode
VAPI_PRIVATE_KEY=demo_mode
```

2. Dit zal de applicatie in demo mode draaien zonder echte voice calls.

## ✅ Verificatie

Na het instellen van de environment variables:
- ✅ Nari Dia TTS server draait op `localhost:7860`
- ✅ Next.js server draait op `localhost:3000`
- ✅ Geen CORS errors meer
- ✅ Voice selection werkt correct

## 🆘 Hulp nodig?

Als je nog steeds problemen hebt:
1. Controleer of beide servers draaien: `ps aux | grep -E "(python3 nari-dia-server|next-server)"`
2. Test de Nari Dia server: `curl http://localhost:7860/health`
3. Controleer de browser console voor specifieke error messages 