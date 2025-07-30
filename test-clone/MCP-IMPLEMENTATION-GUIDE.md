# MCP Implementation Guide - Demo Personalisatie

## Overzicht MCP Tools
Voor demo personalisatie gebruiken we twee hoofdtools:
1. **Playwright MCP** - Voor website data extraction
2. **Notion MCP** - Voor database opslag en beheer

## Playwright MCP - Data Gathering Process

### Setup en Browser Navigatie
```bash
# Start met navigeren naar lead website
mcp_playwright_browser_navigate(url: "https://[lead-website].com")

# Wacht tot pagina geladen is
mcp_playwright_browser_wait_for(time: 3)

# Neem screenshot voor visuele referentie
mcp_playwright_browser_take_screenshot(filename: "lead-homepage.png")
```

### Data Extractie Workflow

#### 1. Praktijk Informatie Verzamelen
```bash
# Snapshot van pagina maken voor element identificatie
mcp_playwright_browser_snapshot()

# Zoek naar praktijk naam (meestal in header/title)
# Klik op About Us / Over Ons links
mcp_playwright_browser_click(element: "About link", ref: "[about-link-ref]")

# Verzamel praktijk naam, dokter naam, locatie
# Let op typische elementen: h1, .practice-name, .doctor-name
```

#### 2. Services/Behandelingen Identificeren
```bash
# Navigeer naar services pagina
mcp_playwright_browser_click(element: "Services menu", ref: "[services-ref]")

# Of zoek naar directe service listings
mcp_playwright_browser_snapshot()

# Identificeer alle behandelingen:
# - Chiropractic care
# - Physical therapy  
# - Massage therapy
# - Specialized treatments
# - Pain management
# etc.
```

#### 3. Branding Kleuren Analyse (KRITIEK!)
```bash
# Homepage screenshot voor primaire branding
mcp_playwright_browser_take_screenshot(filename: "lead-homepage-branding.png")

# Services pagina voor kleur consistentie
mcp_playwright_browser_navigate(url: "https://[lead-website].com/services")
mcp_playwright_browser_take_screenshot(filename: "lead-services-branding.png")

# About pagina voor professionele kleuren
mcp_playwright_browser_navigate(url: "https://[lead-website].com/about")
mcp_playwright_browser_take_screenshot(filename: "lead-about-branding.png")

# Contact pagina voor header/footer kleuren
mcp_playwright_browser_navigate(url: "https://[lead-website].com/contact")
mcp_playwright_browser_take_screenshot(filename: "lead-contact-branding.png")
```

**Kleurenanalyse Process:**
1. **Screenshot Analysis** → Identificeer primaire/secundaire kleuren
2. **Praktijk Type** → Bepaal branding stijl (Traditional/Modern/Luxury/Family)
3. **Tailwind Mapping** → Plan emerald/teal → [nieuwe kleuren] replacement
4. **Color Scheme Examples**:
   - **Traditional Chiropractic** → Blue/Indigo (trust, professional)
   - **Wellness/Holistic** → Emerald/Teal (nature, healing) 
   - **Sports Medicine** → Orange/Red (energy, strength)
   - **Luxury Spa** → Purple/Gold (luxury, exclusive)
   - **Family Practice** → Rose/Pink (warm, friendly)

#### 4. Contact en Locatie Info
```bash
# Ga naar contact pagina
mcp_playwright_browser_navigate(url: "https://[lead-website].com/contact")

# Verzamel locatie informatie (maar gebruik NIET in demo)
# Identificeer stad/staat voor personalisatie
```

### Data Extractie Resultaat Format
Na Playwright data gathering, structureer informatie als:
```json
{
  "practice_name": "Advanced Wellness Center",
  "doctor_name": "Dr. John Smith, DC",
  "location": "Austin, TX",
  "services": [
    "Chiropractic Adjustments",
    "Physical Therapy", 
    "Massage Therapy",
    "Sports Medicine"
  ],
  "brand_colors": {
    "primary": "#2563eb",
    "secondary": "#1d4ed8", 
    "accent": "#3b82f6",
    "tailwind_mapping": {
      "emerald-600": "blue-600",
      "teal-600": "indigo-600",
      "emerald-50": "blue-50",
      "teal-50": "indigo-50"
    }
  },
  "website_url": "https://example-practice.com"
}
```

## Notion MCP - Database Management

### Database Setup
Eerst verbinden met "Demo Pages" database:
```bash
# Zoek naar bestaande Demo Pages database
mcp_notionApi_API-post-search(query: "Demo Pages")

# Als niet gevonden, maak nieuwe database aan
mcp_notionApi_API-create-a-database(
  parent: {"type": "page_id", "page_id": "[workspace-page-id]"},
  title: [{"type": "text", "text": {"content": "Demo Pages"}}],
  properties: {
    // Database schema zoals gedefinieerd in documentatie
  }
)
```

### Record Aanmaken voor Nieuwe Lead
```bash
# Maak nieuwe pagina in Demo Pages database
mcp_notionApi_API-post-page(
  parent: {"page_id": "[demo-pages-db-id]"},
  properties: {
    "title": [{"type": "text", "text": {"content": "[Lead Name]"}}],
    "type": "title"
  }
)
```

### Eigenschappen Invullen
```bash
# Update pagina met alle verzamelde informatie
mcp_notionApi_API-patch-page(
  page_id: "[new-page-id]",
  properties: {
    "Praktijk Naam": {
      "rich_text": [{"text": {"content": "Advanced Wellness Center"}}]
    },
    "Dokter Naam": {
      "rich_text": [{"text": {"content": "Dr. John Smith, DC"}}]
    },
    "Locatie": {
      "rich_text": [{"text": {"content": "Austin, TX"}}]
    },
    "Website URL": {
      "url": "https://example-practice.com"
    },
    "Demo URL": {
      "url": "https://advanced-wellness.loca.lt/"
    },
    "Agent Prompt": {
      "rich_text": [{"text": {"content": "You are Robin, scheduling assistant at Advanced Wellness..."}}]
    },
    "First Message": {
      "rich_text": [{"text": {"content": "Thank you for calling Advanced Wellness! This is Robin..."}}]
    },
    "Agent ID": {
      "rich_text": [{"text": {"content": ""}}]
    },
    "Wachtwoord": {
      "rich_text": [{"text": {"content": "192.168.1.100"}}]
    },
    "Status": {
      "select": {"name": "Draft"}
    }
  }
)
```

### Services als Multi-Select Toevoegen
```bash
# Voor elke service, voeg toe aan multi-select
mcp_notionApi_API-patch-page(
  page_id: "[page-id]",
  properties: {
    "Services": {
      "multi_select": [
        {"name": "Chiropractic Adjustments"},
        {"name": "Physical Therapy"},
        {"name": "Massage Therapy"},
        {"name": "Sports Medicine"}
      ]
    }
  }
)
```

### Notities en Extra Info
```bash
# Voeg gedetailleerde notities toe
mcp_notionApi_API-patch-page(
  page_id: "[page-id]",
  properties: {
    "Notities": {
      "rich_text": [
        {
          "text": {
            "content": "Personalisatie details:\n- Brand kleuren: blauw theme\n- Focus op sports medicine\n- Modern website design\n- Target audience: athletes"
          }
        }
      ]
    }
  }
)
```

## Agent Prompt & First Message Generatie

### Voice & Chat Agent Personalisatie
Voor elke nieuwe lead worden automatisch gepersonaliseerde prompts voor BEIDE agents gegenereerd en opgeslagen in Notion:

**DUAL AGENT SYSTEM:**
1. **Voice Agent (ElevenLabs)**: Telefoon-gebaseerde interacties  
2. **Chat Agent (OpenAI GPT-4)**: Website chat interface

**GECENTRALISEERD CONFIGURATIESYSTEEM:**
Het systeem gebruikt `/src/lib/practice-config.ts` voor consistente agent personalisatie:
```typescript
// Automatische agent configuratie gebaseerd op URL/port
const practiceConfig = getCurrentPractice();
// Levert correcte prompts voor voice EN chat agents
```

**ElevenLabs Voice Agent Prompt Template:**
```
You are Robin, [ROLE] assistant at [PRACTICE_NAME] in [LOCATION]. Help [PATIENTS/CLIENTS] schedule with [DOCTOR_NAME].

RULES:
- Ask ONE question at a time
- Use friendly, conversational language
- Collect: name, phone, email
- Never ask location (only ONE location)

LOCATION: [FULL_ADDRESS]

TREATMENTS:
[PRACTICE_SPECIFIC_SERVICES_LIST]

FLOW: Treatment → Name → Phone → Email → Confirm

CONFIRMATION: "Perfect! I have you scheduled for [TREATMENT] with [DOCTOR_NAME] at [PRACTICE_NAME] in [LOCATION]. We'll send confirmation to [EMAIL] and call [PHONE]. [DOCTOR_NAME] looks forward to helping you!"
```

**ElevenLabs First Message Template:**
```
Thank you for calling [PRACTICE_NAME]! This is Robin, your [ROLE] assistant. We're here to help you [GOAL] with [DOCTOR_NAME]. Which of our [SERVICES_TYPE] can I help you schedule today?
```

**OpenAI Chat Agent System Prompt Template:**
```
You are Robin, the helpful [ROLE] at [PRACTICE_NAME] in [LOCATION]. You help patients schedule appointments with [DOCTOR_NAME] through the website chat.

PERSONALITY:
- Professional but warm and friendly
- Patient and helpful 
- Knowledgeable about all treatments
- Clear communicator

SERVICES OFFERED:
[PRACTICE_SPECIFIC_SERVICES_LIST]

BOOKING PROCESS:
1. Ask what service they're interested in
2. Collect name and phone number
3. Suggest they call to complete booking
4. Provide practice phone number

LOCATION: [PRACTICE_NAME] has only ONE location in [LOCATION]

Always end conversations by encouraging them to call the practice directly for final appointment scheduling.
```

**Chat Initial Message Template:**
```
Hello! I'm Robin, your virtual assistant for [PRACTICE_NAME]. I'm here to help you learn about our [SERVICES_TYPE] and guide you toward scheduling with [DOCTOR_NAME]. What brings you in today? 😊
```

**Automatische Personalisatie per Type:**
- **Chiropractic**: "scheduling assistant", "achieve better health", "treatments"
- **Wellness Center**: "wellness assistant", "begin your healing journey", "wellness treatments"

### Lead-specifieke Prompt Pagina's
**Notion Character Limit Oplossing:**
Agent prompts kunnen langer zijn dan de 2000 karakter limiet van Notion Rich Text velden. Daarom gebruikt het systeem een twee-tier aanpak:

1. **Database Versie**: Verkorte prompt voor overzicht (max 2000 chars)
2. **Lead-specifieke Pagina**: Complete prompt zonder limiet

**Workflow voor Full Prompts:**
```bash
# 1. Maak lead-specifieke pagina voor volledige prompts
mcp_notionApi_API-post-page(
  parent: {"page_id": "[workspace-root-id]"},
  properties: {
    "title": [{"type": "text", "text": {"content": "[Practice Name] - Complete Agent Prompt"}}],
    "type": "title"
  }
)

# 2. Vul pagina met lead informatie en volledige prompt
mcp_notionApi_API-patch-block-children(
  block_id: "[new-page-id]",
  children: [
    {
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "🏥 [PRACTICE NAME] - [LOCATION]"}}]
      }
    },
    {
      "type": "paragraph", 
      "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "Dr. [Name] | [Address]"}}]
      }
    },
    {
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "Agent ID: [Agent ID]"}}]
      }
    },
    {
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "📞 FIRST MESSAGE:"}}]
      }
    },
    {
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "[Complete First Message]"}}]
      }
    },
    {
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "🤖 COMPLETE AGENT PROMPT:"}}]
      }
    },
    {
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "[Complete Full Prompt - No Character Limit]"}}]
      }
    }
  ]
)

# 3. Update database entry met link naar volledige prompt pagina
mcp_notionApi_API-patch-page(
  page_id: "[database-entry-id]",
  properties: {
    "Full Prompts": {
      "url": "https://www.notion.so/[page-url]"
    }
  }
)
```

**Voordelen van dit systeem:**
- Database overzicht met verkorte prompts voor snelle referentie
- Volledige prompts opgeslagen zonder karakterlimiet
- Elke lead heeft eigen dedicated pagina
- Makkelijk toegang via database link
- Geen informatie verlies door truncatie  
- **Sports Medicine**: "scheduling assistant", "optimize your performance", "treatments"
- **Family Practice**: "scheduling assistant", "take care of your family's health", "services"

**Notion Opslag:**
```javascript
"Agent Prompt": {
  "rich_text": [{"text": {"content": "[GENERATED_PROMPT_SHORT]"}}]  // Max 2000 chars
},
"First Message": {
  "rich_text": [{"text": {"content": "[GENERATED_FIRST_MESSAGE]"}}]
},
"Agent ID": {
  "rich_text": [{"text": {"content": ""}}]  // Leeg voor handmatige invulling
},
"Full Prompts": {
  "url": "https://www.notion.so/Full-Agent-Prompts-Complete-Versions-..."  // Link naar volledige versies
}
```

**Notion Tekst Limitatie:**
- Rich Text velden hebben een limiet van **2000 karakters**
- Voor volledige prompts wordt een aparte pagina gebruikt
- Database bevat verkorte versie voor overzicht
- Volledige versies beschikbaar via "Full Prompts" link

## Complete Workflow Script

### Stap 1: Data Gathering
```bash
# 1. Navigate to lead website
mcp_playwright_browser_navigate(url: "[lead-website]")

# 2. Extract all information systematically
# 3. Structure data in JSON format
# 4. Save screenshots for reference
```

### Stap 2: Code Personalisatie
```bash
# A. Tekstuele Replacements
sed -i '' 's/SpineAlign Center/[new-practice-name]/g' src/app/page.tsx
sed -i '' 's/Dr\. Sherra Conde/[new-doctor-name]/g' src/app/page.tsx
sed -i '' 's/Fayetteville, GA/[new-location]/g' src/app/page.tsx

# B. Branding Kleuren Replacement (BULK)
# Voor alle emerald varianten:
sed -i '' 's/emerald-50/blue-50/g' src/app/page.tsx src/components/*.tsx
sed -i '' 's/emerald-100/blue-100/g' src/app/page.tsx src/components/*.tsx
sed -i '' 's/emerald-600/blue-600/g' src/app/page.tsx src/components/*.tsx
sed -i '' 's/emerald-700/blue-700/g' src/app/page.tsx src/components/*.tsx

# Voor alle teal varianten:
sed -i '' 's/teal-50/indigo-50/g' src/app/page.tsx src/components/*.tsx
sed -i '' 's/teal-600/indigo-600/g' src/app/page.tsx src/components/*.tsx
sed -i '' 's/teal-700/indigo-700/g' src/app/page.tsx src/components/*.tsx

# C. Services Lists Updaten
# Bewerk handmatig arrays in page.tsx en components

# D. Robin's Introductie Aanpassen
# Update ChatDemo.tsx initial message en resetChat function
```

### Stap 3: Tunnel & Database Update
```bash
# 1. Start nieuwe tunnel
# 2. Test toegankelijkheid
# 3. Create Notion record met alle details
# 4. Update status naar "Live"
```

## Error Handling & Validation

### Website Toegang Problemen
```bash
# Als website niet toegankelijk:
# 1. Check robots.txt
# 2. Try different browser user-agent
# 3. Manual extraction van publieke informatie
# 4. Google search voor praktijk info
```

### Notion Database Fouten
```bash
# Als database niet gevonden:
# 1. Search in alle workspaces
# 2. Check permissions
# 3. Create new database if needed
# 4. Verify property schemas match
```

### Demo Testing Protocol
```bash
# Na elke personalisatie:
# 1. Test tunnel URL + password
# 2. Verify alle praktijk info correct
# 3. Test voice agent responses
# 4. Check mobile responsiveness
# 5. Update Notion status naar "Completed"
```

## Monitoring & Updates

### Lead Engagement Tracking
- Check tunnel access logs
- Monitor conversion metrics
- Update Notion met feedback
- Plan follow-up actions

### Database Maintenance
- Regular backup van Demo Pages
- Archive completed demos
- Update templates based op learnings
- Track ROI per demo type

---

**Key Reminder**: Altijd Playwright gebruiken voor data gathering, nooit manual browsing. Altijd Notion gebruiken voor opslag, zodat alle demo's trackbaar zijn. 