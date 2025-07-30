# Slack AI Bot Setup Guide

## 🤖 Overzicht
Deze bot integreert OpenAI met Slack via Model Context Protocol (MCP) en kan in verschillende channels worden gebruikt voor AI-assistentie en Slack operaties.

## 🔧 Stap 1: Slack App Configuratie

### 1.1 Slack App Aanmaken
1. Ga naar [api.slack.com/apps](https://api.slack.com/apps)
2. Klik **"Create New App"** → **"From scratch"**
3. Vul app name in: `AI Assistant Bot`
4. Selecteer je workspace
5. Klik **"Create App"**

### 1.2 Bot Token Scopes Configureren
In de app instellingen, ga naar **OAuth & Permissions**:

**Bot Token Scopes toevoegen:**
```
channels:history     - Kanaal berichten lezen
channels:read        - Kanaal informatie lezen
chat:write          - Berichten versturen
chat:write.public   - Berichten in publieke kanalen
reactions:read      - Reacties lezen
reactions:write     - Reacties toevoegen
users:read          - Gebruiker informatie lezen
app_mentions:read   - Mentions lezen
im:history          - DM geschiedenis lezen
im:read             - DM informatie lezen
im:write            - DMs versturen
commands            - Slash commands
```

### 1.3 Event Subscriptions
Ga naar **Event Subscriptions** en schakel in:
- **Subscribe to bot events:**
  - `app_mention`
  - `message.im`
  - `message.channels`

### 1.4 Socket Mode (Aanbevolen voor development)
1. Ga naar **Socket Mode** 
2. Schakel **"Enable Socket Mode"** in
3. Geef het een naam: `AI Bot Socket`
4. Kopieer de **App-Level Token** (xapp-...)

### 1.5 Slash Commands (Optioneel)
Ga naar **Slash Commands** en voeg toe:
- Command: `/ai`
- Request URL: `https://your-app.com/slack/events` (niet nodig bij Socket Mode)
- Short Description: `Ask AI Assistant`
- Usage Hint: `[your question]`

### 1.6 App Installeren
1. Ga naar **OAuth & Permissions**
2. Klik **"Install to Workspace"**
3. Kopieer de **Bot User OAuth Token** (xoxb-...)

## 🔑 Stap 2: Environment Variables

Maak een `.env` bestand in de root van je project:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Slack Bot Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-from-oauth-permissions
SLACK_SIGNING_SECRET=your-signing-secret-from-basic-information
SLACK_APP_TOKEN=xapp-your-app-token-from-socket-mode

# Server Configuration
PORT=3000
NODE_ENV=development
LOG_LEVEL=info
```

**Waar vind je deze tokens:**
- `SLACK_BOT_TOKEN`: OAuth & Permissions → Bot User OAuth Token
- `SLACK_SIGNING_SECRET`: Basic Information → Signing Secret
- `SLACK_APP_TOKEN`: Socket Mode → App-Level Token

## 🚀 Stap 3: Bot Starten

### 3.1 Dependencies Installeren
```bash
npm install
```

### 3.2 MCP Server Bouwen
```bash
npm run mcp:build
```

### 3.3 Bot Starten
```bash
npm run slack:dev
```

De bot start automatisch de MCP server en connecteert met Slack.

## 💬 Stap 4: Bot Gebruiken

### 4.1 In Channels
1. Voeg de bot toe aan een channel: `/invite @AI Assistant Bot`
2. Mention de bot: `@AI Assistant Bot Hallo, kun je me helpen?`
3. De bot reageert met AI-gegenereerde antwoorden

### 4.2 Direct Messages
1. Stuur een DM naar de bot
2. Typ je vraag direct, geen @ nodig
3. De bot reageert automatisch

### 4.3 Slash Commands
```
/ai Wat is het weer vandaag?
```

### 4.4 MCP Commands
De bot herkent specifieke commando's voor Slack operaties:

```
toon kanalen                    - Lijst alle kanalen
stuur bericht naar #general: Hallo!   - Stuur bericht naar kanaal
toon geschiedenis van #general  - Toon recente berichten
info over @gebruiker           - Gebruikersinfo opvragen
```

## 🔧 Stap 5: Geavanceerde Configuratie

### 5.1 Productiemodus
Voor productie gebruik:
```bash
NODE_ENV=production npm start
```

### 5.2 Docker Deployment
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
RUN npm run mcp:build
EXPOSE 3000
CMD ["npm", "run", "slack:dev"]
```

### 5.3 Cloud Deployment (Railway/Render)
1. Connect je GitHub repository
2. Stel environment variables in via dashboard
3. Deploy automatisch bij git push

## 🛠️ Troubleshooting

### Bot Reageert Niet
1. **Check tokens**: Controleer of alle tokens correct zijn
2. **Check scopes**: Zorg dat alle benodigde scopes zijn toegevoegd  
3. **Check logs**: Kijk in `slack-bot.log` voor errors
4. **Test connection**: Gebruik `/invite @bot` in een test channel

### MCP Connection Errors
1. **Build MCP server**: `npm run mcp:build`
2. **Check permissions**: Zorg dat dist/mcp-server/index.js bestaat
3. **Environment variables**: Controleer SLACK_BOT_TOKEN voor MCP server

### OpenAI API Errors  
1. **API Key**: Controleer OPENAI_API_KEY
2. **Rate limits**: Mogelijk API quota bereikt
3. **Model availability**: Zorg dat gpt-4o-mini beschikbaar is

## 📊 Monitoring

De bot logt naar:
- Console (development)
- `slack-bot.log` bestand
- Bevat timestamps, errors, en tool usage

## 🎯 Features

### AI Capabilities
✅ **Nederlandse conversaties** met OpenAI GPT-4o-mini  
✅ **Context-aware responses** met channel/user info  
✅ **Multi-channel support** - werkt in alle channels  
✅ **Direct message support** - privé gesprekken  
✅ **Thread responses** - houdt discussies georganiseerd  

### MCP Tools
✅ **list-slack-channels** - Toon alle kanalen  
✅ **post-slack-message** - Verstuur berichten  
✅ **get-slack-history** - Ophalen chat geschiedenis  
✅ **get-slack-user-info** - Gebruikersinfo opvragen  

### Command Parsing
✅ **Natural language** - "toon kanalen", "stuur bericht naar #general"  
✅ **Intelligent routing** - AI + MCP tools gecombineerd  
✅ **Error handling** - Graceful fallbacks bij problemen  

## 🔐 Security

- Tokens worden via environment variables geladen
- Geen gevoelige data in code
- Request validation via Slack signing secret
- Rate limiting via OpenAI SDK

## 📈 Next Steps

1. **Extend MCP Tools**: Voeg meer business-specifieke tools toe
2. **Advanced AI**: Implementeer conversation memory
3. **Analytics**: Track usage en performance
4. **Enterprise**: SSO, advanced permissions, audit logging 