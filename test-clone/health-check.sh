#!/bin/bash

# Health Check Script voor Demo Tunnels
# Controleert of tunnels werken en herstart ze indien nodig

LOG_FILE="./logs/health-check.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Zorg dat logs directory bestaat
mkdir -p logs

echo "[$TIMESTAMP] 🔍 Starting health check..." | tee -a "$LOG_FILE"

# Functie om tunnel status te checken
check_tunnel() {
    local url=$1
    local name=$2
    
    # Check of URL bereikbaar is (binnen 10 seconden)
    if curl -s --max-time 10 -o /dev/null -w "%{http_code}" "$url" | grep -q "200\|302\|401"; then
        echo "[$TIMESTAMP] ✅ $name tunnel OK" | tee -a "$LOG_FILE"
        return 0
    else
        echo "[$TIMESTAMP] ❌ $name tunnel FAILED" | tee -a "$LOG_FILE"
        return 1
    fi
}

# Functie om tunnel te herstarten
restart_tunnel() {
    local tunnel_name=$1
    local port=$2
    local subdomain=$3
    
    echo "[$TIMESTAMP] 🔄 Restarting $tunnel_name..." | tee -a "$LOG_FILE"
    
    # Stop oude tunnel
    pm2 delete "$tunnel_name" 2>/dev/null || true
    
    # Wacht even
    sleep 2
    
    # Start nieuwe tunnel
    pm2 start "lt --port $port --subdomain $subdomain" --name "$tunnel_name"
    
    # Wacht tot tunnel gestart is
    sleep 5
    
    echo "[$TIMESTAMP] ✅ $tunnel_name restarted" | tee -a "$LOG_FILE"
}

# Check SpineAlign Center tunnel
if ! check_tunnel "https://spinealign-center.loca.lt/" "SpineAlign Center"; then
    restart_tunnel "tunnel-spinealign" "3000" "spinealign-center"
fi

# Check Smith Chiropractic tunnel  
if ! check_tunnel "https://smith-chiropractic.loca.lt/" "Smith Chiropractic"; then
    restart_tunnel "tunnel-smith" "3001" "smith-chiropractic"
fi

# Check of Next.js services draaien
echo "[$TIMESTAMP] 🔍 Checking Next.js services..." | tee -a "$LOG_FILE"

if ! lsof -i :3000 >/dev/null 2>&1; then
    echo "[$TIMESTAMP] ❌ Port 3000 not responding, restarting SpineAlign demo" | tee -a "$LOG_FILE"
    pm2 restart spinealign-demo
fi

if ! lsof -i :3001 >/dev/null 2>&1; then
    echo "[$TIMESTAMP] ❌ Port 3001 not responding, restarting Smith demo" | tee -a "$LOG_FILE"
    pm2 restart smith-demo
fi

# Status rapportage
echo "[$TIMESTAMP] 📊 Current PM2 status:" | tee -a "$LOG_FILE"
pm2 jlist | jq -r '.[] | "\(.name): \(.pm2_env.status)"' 2>/dev/null || pm2 status | tee -a "$LOG_FILE"

echo "[$TIMESTAMP] ✅ Health check completed" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE" 