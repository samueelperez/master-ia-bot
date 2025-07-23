#!/bin/bash

# Script de inicio específico para Railway
set -e

echo "🚀 Iniciando Backend para Railway..."

# Crear directorios necesarios
mkdir -p /app/logs /app/pids

# Verificar variables críticas
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "⚠️ TELEGRAM_BOT_TOKEN no está configurado (opcional para healthcheck)"
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️ OPENAI_API_KEY no está configurado (opcional para healthcheck)"
fi

echo "✅ Variables de entorno verificadas"

# Iniciar solo el backend (para healthcheck)
echo "🔧 Iniciando Backend..."
cd /app/src/backend

# Verificar que el archivo existe
if [ ! -f "main_secure.py" ]; then
    echo "❌ main_secure.py no encontrado"
    exit 1
fi

# Iniciar el backend
echo "🚀 Ejecutando: python main_secure.py"
python main_secure.py > /app/logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > /app/pids/backend.pid

echo "✅ Backend iniciado con PID: $BACKEND_PID"

# Esperar un poco para que el servicio inicie
echo "⏳ Esperando 10 segundos para que el servicio inicie..."
sleep 10

# Verificar que el servicio esté funcionando
echo "🔍 Verificando que el servicio esté funcionando..."
if curl -f http://localhost:8000/ping > /dev/null 2>&1; then
    echo "✅ Servicio funcionando correctamente"
else
    echo "❌ Servicio no responde"
    echo "📋 Logs del backend:"
    tail -20 /app/logs/backend.log
    exit 1
fi

# Función de limpieza
cleanup() {
    echo "🛑 Deteniendo backend..."
    if [ -f "/app/pids/backend.pid" ]; then
        pid=$(cat "/app/pids/backend.pid")
        kill "$pid" 2>/dev/null || true
    fi
    exit 0
}

# Capturar señales
trap cleanup SIGTERM SIGINT

# Mantener el script ejecutándose
echo "🎉 Backend ejecutándose en puerto 8000..."
echo "📡 Endpoint /ping disponible para Railway healthcheck"

while true; do
    sleep 30
    echo "✅ Backend funcionando - $(date)"
done 