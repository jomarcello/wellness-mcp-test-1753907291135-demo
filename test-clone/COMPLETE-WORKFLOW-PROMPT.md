# 🎯 COMPLETE WORKFLOW PROMPT: Personalized Lead Scraper + Vercel Demo Creator

## 📋 MASTER PROMPT FOR YOUR CODING AGENT

**Copy and paste this entire prompt to your agent to execute the complete workflow**

---

## 🚀 EXECUTE: Complete Lead Discovery + Vercel Demo Creation Workflow

**Goal**: Find chiropractic/wellness practices and create personalized Vercel-hosted demos for each lead.

### 🔍 PHASE 1: LEAD DISCOVERY

**Use Playwright MCP to find leads:**

```
Search for: "chiropractor [CITY] [STATE]" or "wellness center [CITY] [STATE]"
```

**For each lead, extract:**
- **Practice Name** (exact business name)
- **Doctor Name** (full name with credentials: Dr. John Smith, DC)
- **Complete Address** (street, city, state, ZIP)
- **Phone Number** (format: (XXX) XXX-XXXX)
- **Website URL** (full https:// URL)
- **Services List** (from their website/services page)
- **Brand Colors** (primary/secondary from website CSS)
- **Practice Type** (chiropractic, wellness, sports medicine, etc.)

### 🎨 PHASE 2: WEBSITE ANALYSIS

**For each discovered website:**
1. Navigate to website using browser_navigate
2. Take screenshot for visual analysis
3. Extract brand colors from CSS/styles
4. Identify service offerings
5. Note branding tone/style

**Color Extraction Process:**
- Primary color: Main brand color (usually in header/logo)
- Secondary color: Accent color (buttons, highlights)
- Map to Tailwind classes: blue, emerald, purple, orange, etc.

### 🏗️ PHASE 3: PERSONALIZED DEMO CREATION

**Create new demo for each lead:**

1. **Copy Template**: Use current codebase as template
2. **Update Configuration**: Modify `src/lib/practice-config.ts`
3. **Replace Branding**: Update all SpineAlign/Smith references
4. **Apply Colors**: Use extracted brand colors in Tailwind classes
5. **Customize Services**: Replace with lead's actual services

**Configuration Updates Needed:**
```javascript
{
  id: '[practice-slug]',
  name: '[Practice Name]',
  doctor: '[Dr. Name with credentials]',
  location: '[Full address]',
  type: '[chiropractic/wellness]',
  branding: {
    primaryColor: '[mapped-color]',
    tagline: 'Your [Type] Assistant'
  },
  services: [/* lead's actual services */]
}
```

### 🚀 PHASE 4: VERCEL DEPLOYMENT

**Deploy each personalized demo:**

1. **Create Vercel Project**: `[practice-name]-demo.vercel.app`
2. **Set Environment Variables**:
   - PRACTICE_ID=[practice-slug]
   - OPENAI_API_KEY=[provided]
   - ELEVENLABS_API_KEY=[provided]
3. **Deploy**: Use Vercel CLI with --prod flag
4. **Capture URL**: Store final deployment URL

### 📊 PHASE 5: NOTION DATABASE STORAGE

**Store each lead in Notion "Demo Leads" database:**

**Required Fields:**
- **Company**: Practice name
- **Contact Name**: Doctor name with credentials
- **Email**: Contact email (if found)
- **Phone**: Practice phone number
- **Location**: Full address
- **Website URL**: Original website
- **Demo URL**: Vercel deployment URL
- **Brand Colors**: JSON of extracted colors
- **Agent Prompt**: Custom AI prompt
- **First Message**: Voice agent greeting

### 🎯 EXAMPLE EXECUTION

**When I say**: "Find 3 chiropractic practices in Phoenix, AZ"

**You should**:
1. Search Google: "chiropractor Phoenix AZ"
2. Visit top 3 practice websites
3. Extract all required data
4. Create 3 personalized demos
5. Deploy to Vercel
6. Store in Notion
7. Return: "Created demos for [Practice1], [Practice2], [Practice3] at [URLs]"

### 🔧 TECHNICAL REQUIREMENTS

**Before Starting, Ensure:**
- Vercel CLI installed: `npm i -g vercel`
- Vercel account authenticated: `vercel login`
- API keys available:
  - OpenAI API key
  - ElevenLabs API key
- Notion database "Demo Leads" exists with correct structure

**File Structure for Each Demo:**
```
[practice-name]-demo/
├── src/
│   ├── app/
│   ├── components/
│   └── lib/practice-config.ts (updated)
├── package.json
├── next.config.ts
├── .env.local (with keys)
└── vercel.json
```

### 🚨 ERROR HANDLING

**Common Issues & Solutions:**
- **Color extraction fails**: Use intelligent defaults based on practice type
- **Website blocked**: Try alternative search methods
- **Vercel subdomain taken**: Append numbers or use variations
- **Missing data**: Ask me for clarification on specific fields

### 📋 QUALITY CHECKLIST

**Before marking complete:**
- [ ] Demo loads at Vercel URL
- [ ] Practice name appears correctly throughout
- [ ] Doctor name and credentials accurate
- [ ] Services match lead's actual offerings
- [ ] Brand colors properly applied
- [ ] Voice agent responds with correct practice info
- [ ] All links functional
- [ ] Notion entry complete with all fields

### 💬 COMMUNICATION PROTOCOL

**Ask me when:**
- You need specific search criteria (city, state, practice type)
- API keys are missing
- Brand color mapping is unclear
- Service categorization needs input
- Deployment fails and needs retry strategy

**Report progress:**
- "Found [X] leads in [location]"
- "Extracted data for [practice name]"
- "Deployed demo for [practice name] at [URL]"
- "Completed [X] of [Y] demos"

---

## 🎯 QUICK START COMMANDS

**To execute the workflow:**

1. **Single Lead**: Create demo for one practice
2. **Batch Process**: Find and create demos for multiple practices
3. **Custom Search**: Use specific criteria I provide

**Example prompts you can give me:**
- "Find 5 chiropractors in Scottsdale, AZ"
- "Create demo for Desert Wellness Center with Dr. Sarah Johnson"
- "Search wellness centers in Miami, FL"

---

## 📁 REFERENCE FILES

**Key Files to Reference:**
- `src/lib/practice-config.ts` - Configuration template
- `src/app/page.tsx` - Main demo page
- `COMPLETE-WORKFLOW-PROMPT.md` - This instruction file
- Notion database: "Demo Leads" (ID: 22441ac0-dfef-81a6-9954-cdce1dfcba1d)

**Color Mapping Guide:**
- Blue practices → blue-600, indigo-600
- Green practices → emerald-600, green-600  
- Purple practices → purple-600, violet-600
- Orange practices → orange-600, amber-600
- Red practices → red-600, rose-600

---

**Ready to execute? Give me your search criteria and I'll start the complete workflow!**
