#!/bin/bash

# Setup Monitoring Script
# Configureert automatische health checks via crontab

echo "🔧 Setting up automatic monitoring..."

# Huidige directory 
CURRENT_DIR=$(pwd)
HEALTH_CHECK_SCRIPT="$CURRENT_DIR/health-check.sh"

# Check of health-check.sh bestaat
if [[ ! -f "$HEALTH_CHECK_SCRIPT" ]]; then
    echo "❌ health-check.sh not found in $CURRENT_DIR"
    exit 1
fi

# Maak logs directory
mkdir -p logs

# Crontab entry voor elke 5 minuten
CRON_ENTRY="*/5 * * * * $HEALTH_CHECK_SCRIPT >/dev/null 2>&1"

# Check of crontab entry al bestaat
if crontab -l 2>/dev/null | grep -q "$HEALTH_CHECK_SCRIPT"; then
    echo "⚠️  Monitoring already configured for this script"
else
    # Voeg crontab entry toe
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo "✅ Added crontab entry: Health check every 5 minutes"
fi

# PM2 startup configureren voor automatische herstart na reboot
echo "🔄 Configuring PM2 startup..."
pm2 startup 2>/dev/null || echo "⚠️  PM2 startup configuration may need manual setup"

echo ""
echo "✅ Monitoring setup completed!"
echo ""
echo "📋 Configuration Summary:"
echo "• Health checks run every 5 minutes"
echo "• Logs saved to: $CURRENT_DIR/logs/health-check.log"
echo "• PM2 configured for auto-restart after reboot"
echo ""
echo "🔧 Useful commands:"
echo "• crontab -l                    - View crontab entries"
echo "• tail -f logs/health-check.log - Follow health check logs" 
echo "• pm2 monit                     - Real-time PM2 monitoring"
echo ""
echo "🚫 To remove monitoring:"
echo "• crontab -e (remove the health-check.sh line)" 