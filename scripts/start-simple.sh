#!/bin/bash

# Script de inicio simple para Railway
set -e

echo "🚀 Iniciando Crypto AI Bot..."

# Crear directorios necesarios
mkdir -p /app/logs /app/pids

# Verificar variables críticas
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN no está configurado"
    exit 1
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY no está configurado"
    exit 1
fi

echo "✅ Variables de entorno verificadas"

# Iniciar servicios en paralelo
echo "🔄 Iniciando servicios..."

# Backend
echo "🔧 Iniciando Backend..."
cd /app/src/backend
python main_secure.py > /app/logs/backend.log 2>&1 &
echo $! > /app/pids/backend.pid

# AI Module
echo "🤖 Iniciando AI Module..."
cd /app/src/ai-module
python main.py > /app/logs/ai-module.log 2>&1 &
echo $! > /app/pids/ai-module.pid

# Data Service
echo "📊 Iniciando Data Service..."
cd /app/src/data-service
python main.py > /app/logs/data-service.log 2>&1 &
echo $! > /app/pids/data-service.pid

# Telegram Bot
echo "📱 Iniciando Telegram Bot..."
cd /app/src/telegram-bot
python -m core.telegram_bot_secure > /app/logs/telegram-bot.log 2>&1 &
echo $! > /app/pids/telegram-bot.pid

# Webapp (opcional)
if [ "$WEBAPP_ENABLED" = "true" ]; then
    echo "🌐 Iniciando Webapp..."
    cd /app/src/webapp
    npm start > /app/logs/webapp.log 2>&1 &
    echo $! > /app/pids/webapp.pid
fi

echo "✅ Todos los servicios iniciados"

# Función de limpieza
cleanup() {
    echo "🛑 Deteniendo servicios..."
    for pid_file in /app/pids/*.pid; do
        if [ -f "$pid_file" ]; then
            pid=$(cat "$pid_file")
            kill "$pid" 2>/dev/null || true
        fi
    done
    exit 0
}

# Capturar señales
trap cleanup SIGTERM SIGINT

# Mantener el script ejecutándose
echo "🎉 Crypto AI Bot ejecutándose..."
while true; do
    sleep 30
    echo "✅ Servicios funcionando - $(date)"
done 