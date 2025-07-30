#!/bin/bash

# Vercel Multi-Deploy Solution
# Creates branch deployments with public access

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

echo "🚀 Vercel branch deployment for: $CLIENT_NAME"
echo "📍 Branch: $BRANCH_NAME"

# Create branch
git checkout main
git pull origin main
git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"

# Update practice config
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

# Ensure public vercel.json
cat > vercel.json << EOF
{
  "version": 2,
  "public": true,
  "buildCommand": "npm run build",
  "outputDirectory": ".next"
}
EOF

# Commit and push
git add .
git commit -m "Deploy $CLIENT_NAME demo - $PRACTICE_TYPE practice" || echo "No changes to commit"
git push origin "$BRANCH_NAME"

# Deploy with Vercel CLI
if command -v vercel &> /dev/null; then
    echo "🚀 Deploying to Vercel..."
    vercel --prod --token="$VERCEL_TOKEN" 2>/dev/null || vercel --prod
    
    echo "✅ Deployed to Vercel!"
    echo "🌐 URL will be: https://agentsdemo-git-$BRANCH_NAME-yourusername.vercel.app"
else
    echo "⚠️  Vercel CLI not installed"
    echo "📋 Install: npm install -g vercel"
    echo "📋 Then run: vercel login"
fi

echo ""
echo "📋 Demo Info:"
echo "   Client: $CLIENT_NAME"
echo "   Branch: $BRANCH_NAME"
echo "   Platform: Vercel branch deployment"