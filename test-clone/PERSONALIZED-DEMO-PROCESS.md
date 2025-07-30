# Gepersonaliseerde Demo Pages - Proces Documentatie

## Overzicht
Dit document beschrijft het volledige proces voor het maken van gepersonaliseerde demo pages voor elke nieuwe lead. De basis demo (SpineAlign Center) wordt aangepast naar de specifieke praktijk van de lead.

## Basis Setup - SpineAlign Center Demo
- **Huidige URL**: https://spinealign-center.loca.lt/
- **Wachtwoord**: 217.103.9.12
- **Basis Template**: `/src/app/page.tsx` en `/src/components/`
- **Tunnel Command**: `lt --port 3000 --subdomain spinealign-center`

## Proces voor Nieuwe Gepersonaliseerde Demo

### Stap 1: Lead Informatie Verzamelen
**AI gebruikt Playwright MCP voor data gathering:**
- Website van de praktijk bezoeken
- Praktijk naam, locatie, specialisaties verzamelen
- Services/behandelingen identificeren
- Dokter naam(en) en credentials
- **Branding kleuren en stijl analyseren** (KRITIEK!)
- Contact informatie (zonder deze in demo te tonen)

**Branding Kleuren Proces:**
```bash
mcp_playwright_browser_navigate(url: "[lead-website]")
mcp_playwright_browser_take_screenshot()
mcp_playwright_browser_snapshot()
```
- **Website screenshot maken** voor visuele analyse
- **Primaire en secundaire kleuren identificeren**
- **Kleurenschema mapping** naar Tailwind CSS classes

### Stap 2: Demo Personalisatie
**Code aanpassingen maken:**
- Praktijk naam vervangen (alle SpineAlign Center references)
- Dokter naam vervangen (Dr. Sherra Conde → nieuwe dokter)
- Locatie updaten (Fayetteville, GA → nieuwe locatie)
- Services lijst aanpassen naar praktijk specifieke behandelingen
- Kleurenschema aanpassen naar praktijk branding
- Robin's introductie aanpassen naar nieuwe praktijk context

**Bestanden om aan te passen:**
- `/src/app/page.tsx` - Hoofdpagina content
- `/src/components/VoiceDemo.tsx` - Voice interface
- `/src/components/ChatDemo.tsx` - Chat interface en Robin's berichten

### Stap 3: Unieke Tunnel Setup
**Voor elke lead een eigen tunnel:**
```bash
lt --port 3000 --subdomain [praktijk-naam-lead]
```
- **URL Format**: `https://[praktijk-naam-lead].loca.lt/`
- **Wachtwoord**: Het IP-adres dat localtunnel genereert
- **Subdomain**: Gebaseerd op praktijk naam (lowercase, geen spaties)

### Stap 4: Notion Database Opslag
**AI gebruikt Notion MCP om op te slaan in "Demo Pages" database:**

**Database Structure:**
- **Company** (Title): Naam van de lead/praktijk
- **Contact Name** (Rich Text): Hoofddokter naam en credentials
- **Email** (Email): Contact email
- **Phone** (Phone): Contact telefoonnummer
- **Location** (Rich Text): Stad, staat
- **Website URL** (URL): Werkelijke website van de praktijk voor branding analyse
- **Demo URL** (URL): Volledige localtunnel URL
- **Password** (Rich Text): Tunnel wachtwoord
- **Brand Colors** (Rich Text): Kleuren analyse van de praktijk
- **Agent Prompt** (Rich Text): Gepersonaliseerde ElevenLabs agent prompt (verkort - max 2000 karakters)
- **First Message** (Rich Text): Openingsbericht van de voice agent
- **Agent ID** (Rich Text): ElevenLabs Agent ID (leeg veld, handmatig in te vullen)
- **Full Prompts** (URL): Link naar lead-specifieke pagina met volledige agent prompts

### Stap 5: Demo Testen
**Verificatie checklist:**
- [ ] Tunnel is bereikbaar met wachtwoord
- [ ] Praktijk naam overal correct vervangen
- [ ] Dokter naam correct weergegeven
- [ ] Services lijst accuraat en compleet
- [ ] Voice agent reageert met juiste praktijk context
- [ ] Chat demo toont correcte informatie
- [ ] Branding kleuren toegepast
- [ ] Geen referenties naar oude praktijk

## Technische Details

### Code Templates
**Belangrijkste vervangingen:**
```javascript
// Van:
"SpineAlign Center" → "[Nieuwe Praktijk Naam]"
"Dr. Sherra Conde" → "[Nieuwe Dokter]"
"Fayetteville, GA" → "[Nieuwe Locatie]"
"Robin" → "[Optioneel: andere AI naam]"

// Services array aanpassen:
const services = [
  { name: '[Service 1]', description: '[Beschrijving]' },
  // ... aangepast naar praktijk specifiek
];
```

### Kleuren Systeem
**Basis Template kleuren (SpineAlign):**
- Primary: `emerald-600` (groen) 
- Secondary: `teal-600` (blauwgroen)
- Background: `emerald-50`, `teal-50`, `green-100`

**Kleurenschema Mapping voorbeelden:**

**1. Traditionele Chiropractic (Smith Chiropractic):**
```bash
emerald-600 → blue-600    # Primair
teal-600 → indigo-600     # Secundair  
emerald-50 → blue-50      # Achtergrond
emerald-100 → blue-100    # Licht accent
```

**2. Sports Medicine Praktijk:**
```bash
emerald-600 → orange-600  # Energie
teal-600 → red-600        # Kracht
emerald-50 → orange-50    # Warm
```

**3. Luxury Wellness Spa:**
```bash
emerald-600 → purple-600  # Luxe
teal-600 → violet-600     # Exclusief
emerald-50 → purple-50    # Elegant
```

**4. Family Practice:**
```bash
emerald-600 → rose-600    # Warm
teal-600 → pink-600       # Vriendelijk  
emerald-50 → rose-50      # Zacht
```

**Automatische Kleur Replacement:**
```bash
# Gebruik sed commands voor bulk replacement:
sed -i '' 's/emerald-600/blue-600/g' src/app/page.tsx
sed -i '' 's/teal-600/indigo-600/g' src/app/page.tsx
# Herhaal voor alle componenten
```

### Voice & Chat Agent Personalisatie
**Robin's persona aanpassen (BEIDE voice EN chat):**
- **Voice Agent (ElevenLabs)**: Introductie bericht en telefoon interactie
- **Chat Agent (OpenAI)**: Chat interface in `ChatDemo.tsx` component
- Praktijk specifieke knowledge voor beide agents
- Treatment lijst en beschrijvingen consistent tussen voice/chat
- Professional tone matching praktijk stijl

**BELANGRIJKE CONFIGURATIE:**
Het systeem gebruikt nu een **gecentraliseerd configuratiesysteem** (`src/lib/practice-config.ts`) dat automatisch de juiste prompts en inhoud levert voor zowel voice als chat agents gebaseerd op de URL/port.

**ElevenLabs Voice Agent Setup:**
- **Agent Prompt**: Gepersonaliseerde prompt met praktijk details
- **First Message**: Openingsbericht aangepast per praktijk
- **Agent ID**: Handmatig aan te maken in ElevenLabs dashboard

**OpenAI Chat Agent Setup:**
- **System Prompt**: Automatisch gegenereerd uit practice configuration
- **Initial Message**: Chat openingsbericht aangepast per praktijk  
- **API Route**: `/api/chat` gebruikt dynamische prompts

**Workflow**: Beide Voice + Chat prompts worden automatisch in Notion opgeslagen

**Prompt Versioning & Organization:**

**Notion Database Limitation**: Rich Text velden hebben een maximale limiet van 2000 karakters. Agent prompts kunnen deze limiet overschrijden.

**Twee-tier Systeem:**
1. **Database Versie**: Verkorte prompt (max 2000 karakters) voor overzicht
2. **Lead-specifieke Pagina**: Complete prompt met alle details

**Lead-specifieke Prompt Pagina's:**
- Elke lead krijgt een eigen Notion pagina: `[Praktijk Naam] - Complete Agent Prompt`
- Bevat: Lead info, Agent ID, First Message, en volledige agent prompt
- Database veld "Full Prompts" linkt naar deze specifieke pagina
- Voordeel: Geen karakter limiet, volledige prompt opslag

**Pagina Structuur:**
```
🏥 [PRAKTIJK NAAM] - [LOCATIE]
Dr. [Naam] | [Adres]
Agent ID: [ElevenLabs Agent ID]

---

📞 FIRST MESSAGE:
[Volledige openingsbericht]

---

🤖 COMPLETE AGENT PROMPT:
[Volledige prompt zonder karakterlimiet]
```

## Workflow Voorbeeld

1. **Input**: Lead informatie (praktijk naam, website URL)
2. **Playwright Data Gathering**: Website bezoeken, info extraheren  
3. **Code Personalisatie**: Template aanpassen naar lead
4. **Dual Agent Configuratie**: 
   - **Practice Config Update**: `src/lib/practice-config.ts` bijwerken met nieuwe lead
   - **Voice Agent Prompts**: ElevenLabs prompt en first message genereren
   - **Chat Agent Prompts**: OpenAI system prompt en initial message genereren
5. **Tunnel Setup**: Nieuwe subdomain maken
6. **Notion Opslag**: Alle details opslaan in database (inclusief beide agent prompts)
7. **ElevenLabs Agent**: Handmatig nieuwe voice agent aanmaken met gegenereerde prompt
8. **Testing**: Beide voice EN chat demos testen met nieuwe configuratie

**KRITIEK**: Vergeet niet dat beide agents (voice + chat) automatisch werken via het gecentraliseerde configuratiesysteem in `practice-config.ts`.
10. **Delivery**: URL en wachtwoord aan lead verstrekken

## Automatisering Mogelijkheden

### Toekomstige Verbeteringen
- Script voor automatische code replacement
- Template systeem voor verschillende praktijk types
- Bulk demo generatie workflow
- Automated testing van gepersonaliseerde demos

### Monitoring
- Track demo usage per lead
- Conversion metrics van demo naar klant
- Feedback collection voor verbetering

---

**Belangrijk**: Dit proces zorgt ervoor dat elke lead een volledig gepersonaliseerde ervaring krijgt die aanvoelt alsof het specifiek voor hun praktijk is ontwikkeld, wat de conversion rate significant verhoogt. 