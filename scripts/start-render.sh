#!/bin/bash

# Script de inicio optimizado para Render.com
set -e

echo "🚀 INICIANDO BACKEND EN RENDER"
echo "=============================="

# Crear directorios necesarios
mkdir -p /opt/render/project/src/logs /opt/render/project/src/pids

# Función para logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Verificar variables de entorno
log "🔍 Verificando configuración..."
log "   BACKEND_PORT: ${BACKEND_PORT:-8000}"
log "   ENABLE_DOCS: ${ENABLE_DOCS:-false}"
log "   PYTHON_VERSION: ${PYTHON_VERSION:-3.11}"

# Verificar que estamos en el directorio correcto
cd /opt/render/project/src/backend

log "📁 Directorio actual: $(pwd)"

# Verificar que main_secure.py existe
if [ ! -f "main_secure.py" ]; then
    log "❌ ERROR: main_secure.py no encontrado"
    exit 1
fi

log "✅ main_secure.py encontrado"

# Verificar dependencias
log "🔍 Verificando dependencias..."
python -c "import fastapi, uvicorn, requests" 2>/dev/null && log "✅ Dependencias básicas OK" || log "❌ Faltan dependencias"

# Iniciar backend
log "🚀 Iniciando backend..."
python main_secure.py 