#!/bin/bash

# Script de inicio SOLO para backend en Railway
set -e

echo "🚀 INICIANDO SOLO BACKEND PARA RAILWAY"
echo "======================================"

# Crear directorios necesarios
mkdir -p /app/logs /app/pids /app/debug

# Función para logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a /app/logs/railway_backend.log
}

# Verificar que estamos en el directorio correcto
cd /app/src/backend

log "📁 Directorio actual: $(pwd)"
log "📋 Archivos en directorio:"
ls -la | while read line; do
    log "  $line"
done

# Verificar que main_secure.py existe
if [ ! -f "main_secure.py" ]; then
    log "❌ ERROR: main_secure.py no encontrado"
    exit 1
fi

log "✅ main_secure.py encontrado"

# Verificar configuración de uvicorn
log "🔍 Verificando configuración de uvicorn:"
grep -n "uvicorn.run" main_secure.py | while read line; do
    log "  $line"
done

# Verificar puerto
log "🔍 Verificando configuración de puerto:"
grep -n "port.*8000" main_secure.py | while read line; do
    log "  $line"
done

# Iniciar SOLO el backend
log "🚀 Iniciando backend en puerto 8000..."
python main_secure.py > /app/logs/backend_detailed.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > /app/pids/backend.pid

log "✅ Backend iniciado con PID: $BACKEND_PID"

# Esperar a que el backend esté listo
log "⏳ Esperando a que el backend esté listo..."
for i in {1..30}; do
    log "⏳ Intento $i/30..."
    sleep 2
    
    # Verificar si el proceso sigue vivo
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        log "❌ Backend se detuvo inesperadamente"
        log "📋 Logs del backend:"
        tail -20 /app/logs/backend_detailed.log | while read line; do
            log "  $line"
        done
        exit 1
    fi
    
    # Verificar si responde en el puerto correcto
    if curl -f http://localhost:8000/ping > /dev/null 2>&1; then
        log "✅ Backend responde correctamente en puerto 8000"
        log "🎉 BACKEND LISTO PARA RAILWAY HEALTHCHECK"
        
        # Mantener el proceso vivo
        while kill -0 $BACKEND_PID 2>/dev/null; do
            sleep 10
            log "✅ Backend funcionando - PID: $BACKEND_PID"
        done
        
        log "❌ Backend se detuvo"
        exit 1
    fi
    
    # Verificar puertos en uso cada 5 intentos
    if [ $((i % 5)) -eq 0 ]; then
        log "🔍 Puertos en uso:"
        netstat -tlnp 2>/dev/null | grep :8000 | while read line; do
            log "  $line"
        done
    fi
done

log "❌ Backend no responde después de 60 segundos"
log "📋 Logs del backend:"
tail -30 /app/logs/backend_detailed.log | while read line; do
    log "  $line"
done

exit 1 