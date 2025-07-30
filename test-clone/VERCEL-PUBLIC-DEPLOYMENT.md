# 🔓 Vercel Public Deployment Guide

## Probleem: Vercel Authentication Blokkade
Wanneer je een demo deploy op Vercel, kan het zijn dat bezoekers een login scherm zien in plaats van de demo. Dit gebeurt door Vercel's "Deployment Protection" features.

## ✅ Oplossingen

### 1. Via vercel.json Configuratie
Voeg altijd deze configuratie toe aan je `vercel.json`:

```json
{
  "version": 2,
  "public": true,
  "name": "your-demo-name",
  "builds": [
    {
      "src": "package.json", 
      "use": "@vercel/next"
    }
  ]
}
```

### 2. Via Deployment Script
Gebruik het `deploy-public.sh` script:

```bash
./deploy-public.sh
```

### 3. Via Vercel Dashboard (Handmatig)
1. Ga naar je Vercel project dashboard
2. Klik op **Settings** tab
3. Ga naar **Deployment Protection** 
4. Zet **Vercel Authentication** op **OFF**
5. Zet **Password Protection** op **OFF**
6. Save changes

### 4. Via CLI Flags
Deploy altijd met deze flags:

```bash
vercel --prod --yes --public
```

## 🚨 Voor Elke Nieuwe Demo

**ALTIJD deze stappen volgen:**

1. ✅ Kopieer `vercel.json` template met `"public": true`
2. ✅ Update de `"name"` field voor de nieuwe praktijk
3. ✅ Gebruik `./deploy-public.sh` script
4. ✅ Test de URL in incognito mode
5. ✅ Als nog steeds auth vereist: check Vercel dashboard settings

## 📋 Template vercel.json voor Nieuwe Demo's

```json
{
  "version": 2,
  "name": "[PRACTICE-NAME]-demo",
  "public": true,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "env": {
    "OPENAI_API_KEY": "@openai-api-key",
    "ELEVENLABS_API_KEY": "@elevenlabs-api-key",
    "PRACTICE_ID": "[practice-id]"
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Robots-Tag", 
          "value": "noindex"
        }
      ]
    }
  ]
}
```

## ⚡ Quick Fix Command

Als demo nog steeds auth vereist na deployment:

```bash
# Re-deploy met force public flag
vercel --prod --yes --force --public

# Of via Vercel CLI project update
vercel project add [project-name] --public
```

## 🔄 Voor Bulk Demo Creation

Voor de complete workflow, voeg altijd toe aan elke nieuwe demo:

1. **vercel.json** - Met `"public": true`
2. **deploy-public.sh** - Deployment script  
3. **Test URL** - Altijd testen in incognito
4. **Document URL** - Voor lead tracking

Dit zorgt ervoor dat alle demo's altijd publiek toegankelijk zijn voor prospects! 🎯