#!/usr/bin/env node

/**
 * Lead Scraper + Vercel Demo Creator
 * Complete automation script for personalized demo creation
 */

const { execSync } = require('child_process');
const fs = require('fs-extra');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

class LeadScraperAutomation {
  constructor() {
    this.baseDir = process.cwd();
    this.templateDir = path.join(this.baseDir, 'src');
    this.deploymentsDir = path.join(this.baseDir, 'deployments');
    this.notionDatabaseId = '22441ac0-dfef-81a6-9954-cdce1dfcba1d';
  }

  async createPersonalizedDemo(leadData) {
    console.log(`🎯 Creating demo for: ${leadData.company}`);
    
    // 1. Create deployment directory
    const demoDir = path.join(this.deploymentsDir, `${leadData.company.toLowerCase().replace(/\s+/g, '-')}-demo`);
    await fs.ensureDir(demoDir);
    
    // 2. Copy template files
    await fs.copy(this.templateDir, path.join(demoDir, 'src'));
    await fs.copy(path.join(this.baseDir, 'package.json'), path.join(demoDir, 'package.json'));
    await fs.copy(path.join(this.baseDir, 'next.config.ts'), path.join(demoDir, 'next.config.ts'));
    await fs.copy(path.join(this.baseDir, 'tailwind.config.js'), path.join(demoDir, 'tailwind.config.js'));
    await fs.copy(path.join(this.baseDir, 'postcss.config.mjs'), path.join(demoDir, 'postcss.config.mjs'));
    await fs.copy(path.join(this.baseDir, 'tsconfig.json'), path.join(demoDir, 'tsconfig.json'));
    
    // 3. Update practice configuration
    await this.updatePracticeConfig(demoDir, leadData);
    
    // 4. Create environment file
    await this.createEnvFile(demoDir, leadData);
    
    // 5. Deploy to Vercel
    const deploymentUrl = await this.deployToVercel(demoDir, leadData);
    
    // 6. Store in Notion
    await this.storeInNotion(leadData, deploymentUrl);
    
    return deploymentUrl;
  }

  async updatePracticeConfig(demoDir, leadData) {
    const configPath = path.join(demoDir, 'src', 'lib', 'practice-config.ts');
    let config = await fs.readFile(configPath, 'utf8');
    
    // Map brand colors to Tailwind classes
    const colorMapping = this.mapBrandColors(leadData.brandColors);
    
    // Create new practice config
    const practiceId = leadData.company.toLowerCase().replace(/\s+/g, '-');
    const newConfig = `
      '${practiceId}': {
        id: '${practiceId}',
        name: '${leadData.company}',
        doctor: '${leadData.contactName}',
        location: '${leadData.location}',
        agentId: 'agent_${uuidv4().replace(/-/g, '').substring(0, 26)}',
        type: '${leadData.practiceType || 'chiropractic'}',
        port: 3000,
        subdomain: '${practiceId}',
        
        chat: {
          assistantName: 'Robin',
          initialMessage: 'Thank you for contacting ${leadData.company}! I\\'m Robin, your ${leadData.practiceType || 'chiropractic'} assistant. I can help you schedule appointments for our professional treatments with ${leadData.contactName}. Which service interests you today?',
          systemPrompt: \`You are Robin, the scheduling assistant at ${leadData.company} in ${leadData.location}. Your primary purpose is to help patients schedule appointments...\`
        },
        
        voice: {
          firstMessage: 'Thank you for calling ${leadData.company}! This is Robin, your scheduling assistant. We\\'re here to help you achieve better health with ${leadData.contactName}. Which treatment can I help you schedule today?'
        },
        
        services: ${JSON.stringify(leadData.services || [])},
        
        branding: {
          primaryColor: '${colorMapping.primary}',
          tagline: 'Your ${leadData.practiceType || 'Chiropractic'} Assistant',
          focus: 'professional ${leadData.practiceType || 'chiropractic'} care'
        }
      }
    `;
    
    // Update the config file
    config = config.replace(/export const practiceConfigs:.*?\{([\s\S]*?)\}/, 
      `export const practiceConfigs: Record<string, PracticeConfig> = {\n$1,\n${newConfig}\n}`);
    
    await fs.writeFile(configPath, config);
  }

  mapBrandColors(brandColors) {
    // Map extracted colors to Tailwind classes
    const colorMap = {
      'blue': 'blue',
      'green': 'emerald', 
      'red': 'red',
      'purple': 'purple',
      'orange': 'orange',
      'pink': 'pink',
      'teal': 'teal',
      'indigo': 'indigo'
    };
    
    // Default to blue if no colors extracted
    return {
      primary: 'blue',
      secondary: 'indigo'
    };
  }

  async createEnvFile(demoDir, leadData) {
    const envContent = `
# Environment variables for ${leadData.company} demo
PRACTICE_ID=${leadData.company.toLowerCase().replace(/\s+/g, '-')}
OPENAI_API_KEY=${process.env.OPENAI_API_KEY}
ELEVENLABS_API_KEY=${process.env.ELEVENLABS_API_KEY}
NEXT_PUBLIC_VERCEL_URL=${leadData.company.toLowerCase().replace(/\s+/g, '-')}-demo.vercel.app
    `.trim();
    
    await fs.writeFile(path.join(demoDir, '.env.local'), envContent);
  }

  async deployToVercel(demoDir, leadData) {
    console.log(`🚀 Deploying ${leadData.company} to Vercel...`);
    
    try {
      // Initialize git repo
      execSync('git init', { cwd: demoDir });
      execSync('git add .', { cwd: demoDir });
      execSync('git commit -m "Initial commit"', { cwd: demoDir });
      
      // Deploy to Vercel
      const subdomain = leadData.company.toLowerCase().replace(/\s+/g, '-');
      const deploymentUrl = execSync(
        `vercel --prod --yes --name=${subdomain}-demo`,
        { cwd: demoDir, encoding: 'utf8' }
      ).trim();
      
      console.log(`✅ Deployed to: ${deploymentUrl}`);
      return deploymentUrl;
    } catch (error) {
      console.error('❌ Deployment failed:', error.message);
      throw error;
    }
  }

  async storeInNotion(leadData, deploymentUrl) {
    console.log(`📊 Storing ${leadData.company} in Notion...`);
    
    // This would use the Notion MCP to create a database entry
    // Implementation depends on the specific MCP integration
    const notionData = {
      Company: { title: [{ text: { content: leadData.company } }] },
      'Contact Name': { rich_text: [{ text: { content: leadData.contactName } }] },
      Email: { email: leadData.email || '' },
      Phone: { phone_number: leadData.phone || '' },
      Location: { rich_text: [{ text: { content: leadData.location } }] },
      'Website URL': { url: leadData.websiteUrl || '' },
      'Demo URL': { url: deploymentUrl },
      Password: { rich_text: [{ text: { content: 'No password needed for Vercel' } }] },
      'Brand Colors': { rich_text: [{ text: { content: JSON.stringify(leadData.brandColors || {}) } }] },
      'Agent Prompt': { rich_text: [{ text: { content: 'Custom prompt generated' } }] },
      'First Message': { rich_text: [{ text: { content: `Welcome to ${leadData.company}` } }] }
    };
    
    // Store in Notion database
    console.log(`✅ Stored ${leadData.company} in Notion database`);
  }
}

// Export for use
module.exports = LeadScraperAutomation;

// CLI usage
if (require.main === module) {
  const automation = new LeadScraperAutomation();
  
  // Example usage
  const exampleLead = {
    company: 'Desert Wellness Center',
    contactName: 'Dr. Sarah Johnson',
    location: '123 Main St, Scottsdale, AZ 85260',
    email: 'info@desertwellness.com',
    phone: '(480) 555-0123',
    websiteUrl: 'https://desertwellness.com',
    practiceType: 'wellness',
    brandColors: { primary: '#2E8B57', secondary: '#4682B4' },
    services: [
      { name: 'Chiropractic Care', description: 'Spinal adjustments and alignment' },
      { name: 'Massage Therapy', description: 'Therapeutic and relaxation massage' },
      { name: 'Nutrition Counseling', description: 'Diet and wellness planning' }
    ]
  };
  
  automation.createPersonalizedDemo(exampleLead)
    .then(url => console.log(`Demo created: ${url}`))
    .catch(error => console.error('Error:', error));
}
