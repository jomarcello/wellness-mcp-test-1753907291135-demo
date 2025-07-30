#!/bin/bash

# Netlify Multi-Deploy Solution
# Creates static builds and deploys to unique Netlify URLs

set -e

if [ $# -lt 1 ]; then
    echo "Usage: $0 \"Client Name\" [Practice Type] [Primary Color]"
    exit 1
fi

CLIENT_NAME="$1"
PRACTICE_TYPE="${2:-general}"
PRIMARY_COLOR="${3:-#2563eb}"

# Generate site name
SITE_NAME="$(echo "$CLIENT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/[^a-z0-9-]//g')-demo"

echo "🚀 Netlify deployment for: $CLIENT_NAME"
echo "📍 Site: $SITE_NAME"

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

# Build static version
echo "🔨 Building static site..."
npm run build

# Deploy to Netlify (requires netlify-cli)
if command -v netlify &> /dev/null; then
    echo "🚀 Deploying to Netlify..."
    netlify deploy --prod --dir=out --site="$SITE_NAME" 2>/dev/null || netlify deploy --prod --dir=out --name="$SITE_NAME"
    
    NETLIFY_URL="https://$SITE_NAME.netlify.app"
    echo "✅ Deployed successfully!"
    echo "🌐 URL: $NETLIFY_URL"
else
    echo "⚠️  Netlify CLI not installed"
    echo "📋 Install: npm install -g netlify-cli"
    echo "📋 Then run: netlify login"
fi

echo ""
echo "📋 Demo Ready:"
echo "   Client: $CLIENT_NAME"
echo "   URL: https://$SITE_NAME.netlify.app"
echo "   Type: Static site (no server-side features)"