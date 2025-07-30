#!/bin/bash

# Persistent Demo System Startup Script
# Zorgt ervoor dat alle services altijd draaien

echo "🚀 Starting Persistent Demo System..."

# Installeer PM2 global als het nog niet bestaat
if ! command -v pm2 &> /dev/null; then
    echo "📦 Installing PM2..."
    npm install -g pm2
fi

# Stop alle bestaande PM2 processen voor schone start
echo "🧹 Cleaning up existing processes..."
pm2 stop all 2>/dev/null || true
pm2 delete all 2>/dev/null || true

# Start Next.js applicaties
echo "🔧 Starting Next.js applications..."
pm2 start ecosystem.config.js

# Wacht tot Next.js services volledig opgestart zijn
echo "⏳ Waiting for Next.js services to start..."
sleep 5

# Start localtunnels
echo "🌐 Starting localtunnels..."

# SpineAlign Center tunnel (port 3000)
pm2 start "lt --port 3000 --subdomain spinealign-center" --name "tunnel-spinealign"

# Smith Chiropractic tunnel (port 3001) 
pm2 start "lt --port 3001 --subdomain smith-chiropractic" --name "tunnel-smith"

# PM2 opstartup instellen voor automatische herstart na reboot
pm2 startup
pm2 save

echo "✅ All services started!"
echo ""
echo "📊 Service Status:"
pm2 status

echo ""
echo "🌐 Demo URLs:"
echo "• SpineAlign Center: https://spinealign-center.loca.lt/ (pass: check ecosystem.config.js)"
echo "• Smith Chiropractic: https://smith-chiropractic.loca.lt/ (pass: check ecosystem.config.js)"
echo ""
echo "🔧 Management Commands:"
echo "• pm2 status          - Check service status"
echo "• pm2 restart all     - Restart all services" 
echo "• pm2 logs            - View logs"
echo "• pm2 monit           - Real-time monitoring"
echo ""
echo "🚨 To completely stop: pm2 stop all && pm2 delete all" 