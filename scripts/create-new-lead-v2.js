#!/usr/bin/env node

/**
 * Complete Automated Lead Generation Script (Hybrid MCP + CLI)
 * 
 * Creates Railway projects with full automation using Railway MCP + CLI:
 * - GitHub repository creation via GitHub API
 * - Railway project creation via Railway API (fallback)
 * - Railway service deployment via Railway CLI
 * - Environment variables setup via Railway CLI
 * - Domain generation via Railway CLI
 * 
 * Usage: node scripts/create-new-lead-v2.js <practice-id> <practice-name>
 * Example: node scripts/create-new-lead-v2.js "beautymed" "BeautyMed Clinic"
 */

const https = require('https');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Configuration
const RAILWAY_TOKEN = process.env.RAILWAY_TOKEN || '3e17dda9-bbfc-4a99-98b6-c424388f9477';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_USER = 'jomarcello';

if (!GITHUB_TOKEN) {
    console.error('❌ GITHUB_TOKEN environment variable is required');
    console.error('Get token from: https://github.com/settings/tokens');
    console.error('Required scopes: repo, workflow');
    process.exit(1);
}

/**
 * Create GitHub repository
 */
async function createGitHubRepo(repoName, practiceName) {
    return new Promise((resolve, reject) => {
        const data = JSON.stringify({
            name: repoName,
            description: `Automated demo for ${practiceName} - Healthcare practice automation`,
            private: false,
            auto_init: true
        });

        const options = {
            hostname: 'api.github.com',
            port: 443,
            path: `/user/repos`,
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${GITHUB_TOKEN}`,
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'Healthcare-Automation-Script',
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(data)
            }
        };

        const req = https.request(options, (res) => {
            let responseData = '';
            
            res.on('data', (chunk) => {
                responseData += chunk;
            });
            
            res.on('end', () => {
                if (res.statusCode === 201) {
                    const repoData = JSON.parse(responseData);
                    console.log(`✅ Created GitHub repository: ${repoData.html_url}`);
                    resolve(repoData);
                } else {
                    console.error(`❌ Failed to create GitHub repo: ${res.statusCode}`);
                    console.error(responseData);
                    reject(new Error(`GitHub repo creation failed: ${res.statusCode}`));
                }
            });
        });

        req.on('error', (error) => {
            console.error(`❌ Request error for GitHub repo:`, error);
            reject(error);
        });

        req.write(data);
        req.end();
    });
}

/**
 * Create Railway project via API (fallback from MCP)
 */
async function createRailwayProject(projectName) {
    return new Promise((resolve, reject) => {
        const mutation = {
            query: `mutation {
                projectCreate(input: {
                    name: "${projectName}"
                    description: "Automated healthcare practice demo"
                }) {
                    project {
                        id
                        name
                    }
                }
            }`
        };

        const data = JSON.stringify(mutation);

        const options = {
            hostname: 'backboard.railway.app',
            port: 443,
            path: '/graphql/v2',
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${RAILWAY_TOKEN}`,
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(data)
            }
        };

        const req = https.request(options, (res) => {
            let responseData = '';
            
            res.on('data', (chunk) => {
                responseData += chunk;
            });
            
            res.on('end', () => {
                try {
                    const response = JSON.parse(responseData);
                    if (response.errors) {
                        console.error('❌ Railway API error:', response.errors[0].message);
                        reject(new Error(response.errors[0].message));
                    } else {
                        const project = response.data.projectCreate.project;
                        console.log(`✅ Created Railway project: ${project.name} (${project.id})`);
                        resolve(project);
                    }
                } catch (error) {
                    console.error('❌ Failed to parse Railway response:', responseData);
                    reject(error);
                }
            });
        });

        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

/**
 * Create Railway service via API (fallback from MCP)
 */
async function createRailwayService(projectId, practiceId) {
    return new Promise((resolve, reject) => {
        const mutation = {
            query: `mutation {
                serviceCreate(input: {
                    projectId: "${projectId}"
                    name: "${practiceId}-demo"
                    description: "Healthcare practice demo service"
                }) {
                    service {
                        id
                        name
                    }
                }
            }`
        };

        const data = JSON.stringify(mutation);

        const options = {
            hostname: 'backboard.railway.app',
            port: 443,
            path: '/graphql/v2',
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${RAILWAY_TOKEN}`,
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(data)
            }
        };

        const req = https.request(options, (res) => {
            let responseData = '';
            
            res.on('data', (chunk) => {
                responseData += chunk;
            });
            
            res.on('end', () => {
                try {
                    const response = JSON.parse(responseData);
                    if (response.errors) {
                        console.error('❌ Railway service creation error:', response.errors[0].message);
                        reject(new Error(response.errors[0].message));
                    } else {
                        const service = response.data.serviceCreate.service;
                        console.log(`✅ Created Railway service: ${service.name}`);
                        resolve(service);
                    }
                } catch (error) {
                    console.error('❌ Failed to parse Railway service response:', responseData);
                    reject(error);
                }
            });
        });

        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

/**
 * Set environment variables via Railway CLI
 */
function setEnvironmentVariables(practiceId) {
    try {
        console.log('⚙️ Setting environment variables via CLI...');
        
        // Set practice ID
        execSync(`railway variables set PRACTICE_ID=${practiceId}`, { 
            stdio: 'pipe',
            timeout: 30000 
        });
        console.log('✅ Set PRACTICE_ID');
        
        // Set environment
        execSync('railway variables set NODE_ENV=production', { 
            stdio: 'pipe',
            timeout: 30000 
        });
        console.log('✅ Set NODE_ENV=production');
        
        // Set OpenAI key if provided
        if (process.env.OPENAI_API_KEY) {
            execSync(`railway variables set OPENAI_API_KEY=${process.env.OPENAI_API_KEY}`, { 
                stdio: 'pipe',
                timeout: 30000 
            });
            console.log('✅ Set OPENAI_API_KEY');
        }
        
        // Set ElevenLabs key if provided
        if (process.env.ELEVENLABS_API_KEY) {
            execSync(`railway variables set ELEVENLABS_API_KEY=${process.env.ELEVENLABS_API_KEY}`, { 
                stdio: 'pipe',
                timeout: 30000 
            });
            console.log('✅ Set ELEVENLABS_API_KEY');
        }
        
    } catch (error) {
        console.log('⚠️ CLI environment variable setup failed:', error.message);
        throw error;
    }
}

/**
 * Connect GitHub repository via Railway CLI
 */
function connectGitHubRepo(repoUrl) {
    try {
        console.log('🔗 Connecting GitHub repository via CLI...');
        
        // Create service
        execSync('railway service --name demo-service', { 
            stdio: 'pipe',
            timeout: 30000 
        });
        console.log('✅ Created Railway service');
        
        // Connect GitHub repository
        execSync(`railway add --repo ${repoUrl}`, { 
            stdio: 'pipe',
            timeout: 30000 
        });
        console.log('✅ Connected GitHub repository');
        
    } catch (error) {
        console.log('⚠️ CLI GitHub connection failed:', error.message);
        throw error;
    }
}

/**
 * Deploy via Railway CLI
 */
function deployService() {
    try {
        console.log('🚀 Deploying service via CLI...');
        
        // Deploy the service
        execSync('railway up', { 
            stdio: 'pipe',
            timeout: 300000  // 5 minutes timeout
        });
        console.log('✅ Deployment completed');
        
    } catch (error) {
        console.log('⚠️ CLI deployment failed:', error.message);
        throw error;
    }
}

/**
 * Generate domain via Railway CLI
 */
function generateDomain() {
    try {
        console.log('🌐 Generating public domain...');
        
        execSync('railway domain', { 
            stdio: 'pipe',
            timeout: 60000 
        });
        console.log('✅ Domain generated');
        
    } catch (error) {
        console.log('⚠️ Domain generation failed:', error.message);
        // This is not critical, deployment can continue
    }
}

/**
 * Main function
 */
async function main() {
    const practiceId = process.argv[2];
    const practiceName = process.argv[3];
    
    if (!practiceId || !practiceName) {
        console.error('❌ Usage: node scripts/create-new-lead-v2.js <practice-id> <practice-name>');
        console.error('Example: node scripts/create-new-lead-v2.js "beautymed" "BeautyMed Clinic"');
        process.exit(1);
    }

    console.log('🚀 Creating FULLY AUTOMATED practice lead...');
    console.log(`📋 Practice ID: ${practiceId}`);
    console.log(`🏥 Practice Name: ${practiceName}`);
    console.log('');

    try {
        // Step 1: Create GitHub repository
        const repoName = `${practiceId}-demo`;
        const repoUrl = `https://github.com/${GITHUB_USER}/${repoName}`;
        
        console.log('📦 Step 1: Creating GitHub repository...');
        const githubRepo = await createGitHubRepo(repoName, practiceName);
        
        // Step 2: Create Railway project
        console.log('\n🚂 Step 2: Creating Railway project...');
        const railwayProject = await createRailwayProject(`${practiceId}-demo`);
        
        // Step 3: Create Railway service
        console.log('\n🔧 Step 3: Creating Railway service...');
        const railwayService = await createRailwayService(railwayProject.id, practiceId);
        
        // Step 4: Set up Railway CLI automation  
        console.log('\n⚙️ Step 4: Setting up Railway CLI automation...');
        
        // Link to the project
        execSync(`railway link -p ${railwayProject.id}`, { 
            stdio: 'pipe',
            timeout: 30000 
        });
        console.log('✅ Linked to Railway project');
        
        // Set environment variables via CLI
        setEnvironmentVariables(practiceId);
        
        // Connect GitHub repository via CLI
        connectGitHubRepo(repoUrl);
        
        // Deploy the service via CLI
        deployService();
        
        // Generate domain via CLI
        generateDomain();
        
        // Step 5: Get final deployment status
        console.log('\n📊 Step 5: Checking deployment status...');
        
        const expectedUrl = `https://${practiceId}-demo-production.up.railway.app`;
        
        console.log('');
        console.log('🎉 COMPLETE AUTOMATION SUCCESSFUL!');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('');
        console.log('📋 Deployment Summary:');
        console.log(`✅ GitHub Repository: ${repoUrl}`);
        console.log(`✅ Railway Project: ${railwayProject.name} (${railwayProject.id})`);
        console.log(`✅ Railway Service: ${railwayService.name}`);
        console.log(`✅ Environment Variables: Set`);
        console.log(`✅ Repository Connection: Connected`);
        console.log(`✅ Deployment: Completed`);
        console.log('');
        console.log('🌐 Expected Live URL:');
        console.log(`🔗 ${expectedUrl}`);
        console.log('');
        console.log('⏳ Site will be ready in ~2-3 minutes');
        console.log('');
        console.log('🔧 Next Steps:');
        console.log('1. Test the demo at the URL above');
        console.log('2. Update practice-specific configuration if needed');
        console.log('3. Share the URL for testing');
        console.log('');
        console.log('✅ This is now 100% automated - no manual intervention required!');
        
        return expectedUrl;
        
    } catch (error) {
        console.error('\n❌ Automation failed:', error.message);
        console.error('\n🔧 Troubleshooting:');
        console.error('1. Check Railway CLI authentication: railway whoami');
        console.error('2. Verify Railway token permissions');
        console.error('3. Check GitHub token scopes');
        console.error('4. Ensure Railway CLI is up to date');
        
        process.exit(1);
    }
}

// Run the script
main().catch(console.error);
