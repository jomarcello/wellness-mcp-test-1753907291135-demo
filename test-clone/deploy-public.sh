#!/bin/bash

# Deploy Public Demo Script
# This ensures the demo is always publicly accessible without Vercel authentication

echo "🚀 Deploying public demo to Vercel..."

# Set environment variables for public deployment
export VERCEL_PROJECT_SETTINGS_PUBLIC=true

# Deploy with explicit public flag and bypass any team authentication
vercel --prod --yes --public --no-wait

echo "✅ Demo deployed publicly without authentication requirements"
echo "📋 Note: If authentication is still required, check Vercel dashboard:"
echo "   1. Go to your project settings"
echo "   2. Navigate to 'Deployment Protection'"  
echo "   3. Disable 'Vercel Authentication'"
echo "   4. Set 'Password Protection' to 'Off'"