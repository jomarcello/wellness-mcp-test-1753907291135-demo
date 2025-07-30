#!/bin/bash

# Multi-Deploy Solution for Railway
# Creates Pull Requests to trigger Railway branch deployments

set -e

if [ $# -lt 1 ]; then
    echo "Usage: $0 \"Client Name\" [Practice Type] [Primary Color]"
    exit 1
fi

CLIENT_NAME="$1"
PRACTICE_TYPE="${2:-general}"
PRIMARY_COLOR="${3:-#2563eb}"

# Generate branch name
BRANCH_NAME="demo/$(echo "$CLIENT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/[^a-z0-9-]//g')"
EXPECTED_URL="https://agentsdemo-$(echo "$BRANCH_NAME" | sed 's/\//-/g').up.railway.app"

echo "🚀 Multi-deployment for: $CLIENT_NAME"
echo "📍 Branch: $BRANCH_NAME"
echo "🌐 Expected URL: $EXPECTED_URL"

# Create branch
git checkout main
git pull origin main
git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"

# Simple practice config for this branch
cat > src/lib/practice-config.ts << EOF
export const practiceConfig = {
  name: "$CLIENT_NAME",
  type: "$PRACTICE_TYPE", 
  primaryColor: "$PRIMARY_COLOR",
  
  // Contact info
  phone: "+44 20 7000 0000",
  address: "123 Medical Street, London, UK",
  
  // Branding
  logo: null,
  
  // Services
  services: [
    "General Consultations",
    "Health Screenings", 
    "Treatment Planning", 
    "Follow-up Care"
  ],
  
  // Demo settings
  enableVoiceDemo: true,
  enableChatDemo: true,
  showPricing: true,
  
  // CTA settings
  calendlyUrl: "https://calendly.com/your-calendar-link",
  ctaEnabled: true
};
EOF

# Commit and push
git add .
git commit -m "Deploy $CLIENT_NAME demo - $PRACTICE_TYPE practice" || echo "No changes to commit"
git push origin "$BRANCH_NAME"

# Create Pull Request to trigger Railway deployment
echo "🔄 Creating Pull Request to trigger Railway deployment..."

# Check if gh CLI is available
if command -v gh &> /dev/null; then
    gh pr create --title "Deploy: $CLIENT_NAME Demo" --body "Railway deployment for $CLIENT_NAME - $PRACTICE_TYPE practice" --base main --head "$BRANCH_NAME" 2>/dev/null || echo "PR may already exist"
    echo "✅ Pull Request created - this should trigger Railway branch deployment"
else
    echo "⚠️  GitHub CLI not available"
    echo "📋 Manual step: Create Pull Request on GitHub for branch $BRANCH_NAME"
    echo "🔗 https://github.com/jomarcello/Agentsdemo/compare/main...$BRANCH_NAME"
fi

echo ""
echo "📋 Demo Info:"
echo "   Client: $CLIENT_NAME"
echo "   Branch: $BRANCH_NAME"
echo "   Expected URL: $EXPECTED_URL"
echo "   GitHub PR: https://github.com/jomarcello/Agentsdemo/pulls"
echo ""
echo "⏱️  Railway should detect the PR and create environment"
echo "🔄 Check Railway dashboard: https://railway.app/dashboard"