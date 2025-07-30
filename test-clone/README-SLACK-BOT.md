# 🤖 Slack AI Bot met OpenAI + MCP

Een intelligente Slack bot die OpenAI integreert met Model Context Protocol (MCP) voor geavanceerde Slack operaties.

## ⚡ Quick Start

1. **Slack App configureren** (zie [SLACK-SETUP.md](./SLACK-SETUP.md) voor details)
2. **Environment variabelen instellen** in `.env`
3. **Bot starten**:
   ```bash
   ./start-slack-bot.sh
   ```

## 🎯 Features

### AI Conversaties
- **Nederlandse gesprekken** met OpenAI GPT-4o-mini
- **Multi-channel support** - werkt in alle channels
- **Direct messages** - privé AI assistent
- **Thread responses** - georganiseerde discussies

### MCP Slack Tools
- **`toon kanalen`** - Lijst alle kanalen
- **`stuur bericht naar #kanaal: tekst`** - Verstuur berichten
- **`toon geschiedenis van #kanaal`** - Chat geschiedenis
- **`info over @gebruiker`** - Gebruikersinfo

### Gebruik in Slack
```
# In channels - mention de bot
@AI Assistant Bot Hallo! Kun je de kanalen tonen?

# Direct messages - typ direct
Wat kun je allemaal voor me doen?

# Slash command
/ai Leg uit wat MCP is
```

## 🔧 Development

```bash
# Dependencies installeren
npm install

# MCP server bouwen
npm run mcp:build

# Bot starten (development)
npm run slack:dev

# Logs bekijken
tail -f slack-bot.log
```

## 🚀 Deployment

### Docker
```bash
docker build -f Dockerfile.slack -t slack-ai-bot .
docker run --env-file .env -p 3000:3000 slack-ai-bot
```

### Cloud (Railway/Render)
1. Connect GitHub repository
2. Set environment variables
3. Deploy automatically

## 🛠️ Configuration

### Environment Variables (.env)
```bash
OPENAI_API_KEY=sk-proj-...          # Your OpenAI API key
SLACK_BOT_TOKEN=xoxb-...           # Bot User OAuth Token
SLACK_SIGNING_SECRET=abc123...      # App Signing Secret  
SLACK_APP_TOKEN=xapp-...           # App-Level Token (Socket Mode)
PORT=3000                          # Server port
NODE_ENV=development               # Environment
```

### Slack App Setup
1. **Bot Token Scopes**: `channels:history`, `chat:write`, `app_mentions:read`, `im:history`, `users:read`
2. **Event Subscriptions**: `app_mention`, `message.im`, `message.channels`
3. **Socket Mode**: Enabled (recommended for development)

## 📊 Architecture

```
Slack Workspace ←→ Slack Bot (OpenAI) ←→ MCP Server ←→ Slack API
                                   ↓
                              Slack Tools:
                              - List channels
                              - Post messages  
                              - Get history
                              - User info
```

## 🔍 Troubleshooting

**Bot reageert niet:**
- Check Slack tokens in `.env`
- Verify bot is invited to channel
- Check logs: `tail -f slack-bot.log`

**MCP errors:**
- Run `npm run mcp:build`
- Check if `dist/mcp-server/index.js` exists

**OpenAI errors:**
- Verify `OPENAI_API_KEY` is correct
- Check API quota/limits

## 📚 Documentation

- **[SLACK-SETUP.md](./SLACK-SETUP.md)** - Uitgebreide setup guide
- **[DOCUMENTATION.md](./DOCUMENTATION.md)** - Volledige project documentatie

---

**Ready to chat with AI on Slack!** 🚀 