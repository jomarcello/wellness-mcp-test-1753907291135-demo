# 🚀 Quick Start Guide - Healthcare AI Platform

Get up and running with the **scalable multi-tenant healthcare AI platform** in under 5 minutes. This system is designed to support **hundreds of healthcare practices** for lead generation and practice onboarding.

## 🎯 What You're Installing

This is **not just a demo** - it's a complete **SaaS platform** designed for:
- **Healthcare Lead Generation**: Each lead gets their own practice demo
- **Practice Onboarding**: Instant custom environments for new clients
- **Scalable Architecture**: Foundation to support 100s or 1000s of practices
- **Revenue Generation**: Ready for subscription-based business models

## ⚡ One-Command Setup

```bash
# 1. Clone and install
git clone https://github.com/jomarcello/Agentsdemo.git
cd Agentsdemo
npm install

# 2. Set up environment variables
cp .env.example .env.local
# Edit .env.local with your API keys (see below)

# 3. Start everything
npm run start:all
```

## 🔑 Required API Keys

Edit `.env.local` with your API keys:

```env
# Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key-here

# Get from https://elevenlabs.io/app/settings/api-keys
# Note: ConversationAI access required
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here
```

## 🎯 Access Your Demo

After starting, get your public URLs:
```bash
npm run tunnel:status
```

You'll see something like:
```
SpineAlign Center: https://spinealign-center.loca.lt/
Smith Chiropractic: https://smith-chiropractic.loca.lt/
```

## 🧪 Test Everything

### Voice Agent Testing
1. Open either tunnel URL
2. Click **"Start Call"** button
3. Speak naturally about appointments or services
4. Robin's voice responds with practice-specific information

### Chat Agent Testing
1. Type in the chat interface
2. Try the premade questions
3. Verify practice-specific responses (no cross-contamination)

### Multi-Practice Testing
1. Open both tunnel URLs in separate tabs
2. Test voice/chat on both
3. Confirm different branding, doctors, and services

## 📊 System Status Commands

```bash
# Check all processes
npm run status

# View logs
npm run logs

# Monitor real-time
npm run monit

# Restart if needed
npm run restart:all

# Stop everything
npm run stop:all
```

## 🏥 What You Get

### **SpineAlign Center** (Emerald/Green)
- **Doctor**: Dr. Sherra Conde
- **Services**: 8 wellness services (Chiropractic, Massage, Acupuncture, etc.)
- **Voice Agent**: Robin discussing wellness and holistic care
- **Port**: 3000

### **Smith Chiropractic** (Blue/Indigo)
- **Doctor**: Dr. John Smith
- **Services**: 6 chiropractic services (Adjustments, Sports Injury, etc.)
- **Voice Agent**: Robin discussing chiropractic care
- **Port**: 3001

## 🔧 Common Issues

### "pm2 command not found"
```bash
npm install -g pm2
```

### "Unable to decode audio data"
- This is fixed! The system now uses 16kHz audio (ElevenLabs standard)
- If you still see this, hard refresh your browser (Cmd+Shift+R)

### "Tunnel not working"
```bash
# Check tunnel status
pm2 logs spinealign-tunnel smith-tunnel --lines 5

# Restart tunnels if needed
pm2 restart spinealign-tunnel smith-tunnel
```

### "Wrong practice information"
- This is fixed! The system has 5-layer practice detection
- If you see wrong info, check the console for practice detection logs

## 🎨 Features Included

✅ **Real-time Voice Conversations** (16kHz audio, WebSocket streaming)  
✅ **Multi-Practice Isolation** (Zero cross-contamination)  
✅ **Dynamic Branding** (Auto-adapts per practice)  
✅ **Professional Chat Interface** (GPT-4 powered)  
✅ **Mobile Responsive** (Works on all devices)  
✅ **Healthcare Context** (Appointment scheduling, service info)  
✅ **Production Ready** (PM2 process management)  

## 🚀 Platform Scaling

### **Add New Practices** (Manual for now, automated in next version)
1. **Edit Configuration**: Add new practice to `src/lib/practice-config.ts`
```typescript
newpractice: {
  name: "New Dental Practice",
  doctor: "Dr. Jane Dentist", 
  specialty: "Dental Care",
  branding: { primary: '#blue', secondary: '#lightblue' },
  services: ["Cleanings", "Fillings", "Cosmetic Dentistry"]
}
```

2. **Add PM2 Process**: Update `ecosystem.config.js`
```javascript
{
  name: 'newpractice-server',
  script: 'npm',
  args: 'start',
  env: { PRACTICE_ID: 'newpractice', PORT: 3002 }
}
```

3. **Create Voice Agent**: Set up ElevenLabs ConversationAI agent
4. **Launch**: `pm2 restart ecosystem.config.js`

### **Roadmap to Full Automation**
- **Database Integration**: Store practice configs in database
- **API Endpoints**: Create practices via API calls
- **Admin Dashboard**: Manage 100s of practices visually
- **Auto-Scaling**: Automatic tunnel and voice agent creation

### **Business Applications**
1. **Lead Generation**: Demo-per-prospect system
2. **Practice Onboarding**: Instant client environments  
3. **White-Label SaaS**: Platform for healthcare consultants
4. **Enterprise Sales**: Custom solutions for large organizations

## 📞 Support

- **Documentation**: See `README.md` for complete details
- **Technical Details**: See `DOCUMENTATION.md`
- **Architecture**: Multi-tenant with complete practice isolation
- **Audio Issue**: Fixed - 16kHz sample rate implemented

**Ready to demo to clients!** 🎉

---

**System Status**: 🟢 All systems operational  
**Voice Agent**: ✅ Working perfectly (16kHz audio)  
**Practice Isolation**: ✅ Zero cross-contamination  
**Production Ready**: ✅ Full PM2 configuration 