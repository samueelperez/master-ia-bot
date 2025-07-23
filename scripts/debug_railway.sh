#!/bin/bash

# Script de depuración para Railway
set -e

echo "🔍 INICIANDO DEPURACIÓN DE RAILWAY"
echo "=================================="

# Crear directorios necesarios
mkdir -p /app/logs /app/pids /app/debug

# Función para logging detallado
log_debug() {
    echo "[DEBUG] $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a /app/debug/railway_debug.log
}

# Función para capturar logs del sistema
capture_system_info() {
    log_debug "=== INFORMACIÓN DEL SISTEMA ==="
    log_debug "Hostname: $(hostname)"
    log_debug "User: $(whoami)"
    log_debug "PWD: $(pwd)"
    log_debug "Environment:"
    env | sort | while read line; do
        log_debug "  $line"
    done
    log_debug "Processes:"
    ps aux | head -10 | while read line; do
        log_debug "  $line"
    done
    log_debug "Network:"
    netstat -tlnp 2>/dev/null | head -10 | while read line; do
        log_debug "  $line"
    done
}

# Función para verificar archivos
verify_files() {
    log_debug "=== VERIFICACIÓN DE ARCHIVOS ==="
    
    # Verificar archivos críticos
    critical_files=(
        "/app/src/backend/main_secure.py"
        "/app/scripts/start-railway.sh"
        "/app/railway.toml"
        "/app/requirements/common.txt"
    )
    
    for file in "${critical_files[@]}"; do
        if [ -f "$file" ]; then
            log_debug "✅ $file - EXISTE"
            log_debug "   Size: $(ls -lh "$file" | awk '{print $5}')"
        else
            log_debug "❌ $file - NO EXISTE"
        fi
    done
    
    # Verificar directorios
    log_debug "Directorio /app:"
    ls -la /app/ | while read line; do
        log_debug "  $line"
    done
    
    log_debug "Directorio /app/src:"
    ls -la /app/src/ | while read line; do
        log_debug "  $line"
    done
}

# Función para verificar dependencias
verify_dependencies() {
    log_debug "=== VERIFICACIÓN DE DEPENDENCIAS ==="
    
    # Verificar Python
    log_debug "Python version: $(python --version 2>&1)"
    log_debug "Python path: $(which python)"
    
    # Verificar pip
    log_debug "Pip version: $(pip --version 2>&1)"
    
    # Verificar módulos críticos
    python_modules=(
        "fastapi"
        "uvicorn"
        "requests"
        "psutil"
    )
    
    for module in "${python_modules[@]}"; do
        if python -c "import $module" 2>/dev/null; then
            log_debug "✅ $module - INSTALADO"
        else
            log_debug "❌ $module - NO INSTALADO"
        fi
    done
}

# Función para iniciar backend con logging detallado
start_backend_debug() {
    log_debug "=== INICIANDO BACKEND CON DEBUG ==="
    
    cd /app/src/backend
    
    # Verificar que el archivo existe
    if [ ! -f "main_secure.py" ]; then
        log_debug "❌ main_secure.py no encontrado"
        return 1
    fi
    
    log_debug "✅ main_secure.py encontrado"
    
    # Mostrar contenido del archivo (primeras líneas)
    log_debug "Primeras 20 líneas de main_secure.py:"
    head -20 main_secure.py | while read line; do
        log_debug "  $line"
    done
    
    # Buscar configuración de uvicorn
    log_debug "Buscando configuración de uvicorn:"
    grep -n "uvicorn.run" main_secure.py | while read line; do
        log_debug "  $line"
    done
    
    # Iniciar backend con logging detallado
    log_debug "🚀 Iniciando backend..."
    python main_secure.py > /app/debug/backend_detailed.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > /app/pids/backend.pid
    
    log_debug "✅ Backend iniciado con PID: $BACKEND_PID"
    
    # Esperar y verificar
    for i in {1..30}; do
        log_debug "⏳ Esperando... ($i/30)"
        sleep 2
        
        # Verificar si el proceso sigue vivo
        if ! kill -0 $BACKEND_PID 2>/dev/null; then
            log_debug "❌ Backend se detuvo inesperadamente"
            log_debug "📋 Logs del backend:"
            tail -50 /app/debug/backend_detailed.log | while read line; do
                log_debug "  $line"
            done
            return 1
        fi
        
        # Verificar si responde
        if curl -f http://localhost:8000/ping > /dev/null 2>&1; then
            log_debug "✅ Backend responde en puerto 8000"
            return 0
        fi
        
        # Verificar puertos en uso
        if [ $((i % 5)) -eq 0 ]; then
            log_debug "Puertos en uso:"
            netstat -tlnp 2>/dev/null | grep :8000 | while read line; do
                log_debug "  $line"
            done
        fi
    done
    
    log_debug "❌ Backend no responde después de 60 segundos"
    log_debug "📋 Logs del backend:"
    tail -50 /app/debug/backend_detailed.log | while read line; do
        log_debug "  $line"
    done
    return 1
}

# Función para pruebas de conectividad
test_connectivity() {
    log_debug "=== PRUEBAS DE CONECTIVIDAD ==="
    
    # Probar diferentes URLs
    urls=(
        "http://localhost:8000/ping"
        "http://127.0.0.1:8000/ping"
        "http://0.0.0.0:8000/ping"
        "http://localhost:8000/health"
        "http://127.0.0.1:8000/health"
    )
    
    for url in "${urls[@]}"; do
        log_debug "📡 Probando: $url"
        if curl -f "$url" > /dev/null 2>&1; then
            log_debug "✅ $url - FUNCIONA"
            response=$(curl -s "$url" 2>/dev/null)
            log_debug "   Response: $response"
        else
            log_debug "❌ $url - NO FUNCIONA"
        fi
    done
}

# Función principal
main() {
    log_debug "🚀 Iniciando depuración completa de Railway"
    
    # Capturar información del sistema
    capture_system_info
    
    # Verificar archivos
    verify_files
    
    # Verificar dependencias
    verify_dependencies
    
    # Iniciar backend con debug
    if start_backend_debug; then
        log_debug "✅ Backend iniciado exitosamente"
        
        # Probar conectividad
        test_connectivity
        
        log_debug "🎉 DEPURACIÓN COMPLETADA - TODO FUNCIONA"
        
        # Mantener ejecutándose
        while true; do
            sleep 30
            log_debug "✅ Sistema funcionando - $(date)"
        done
    else
        log_debug "❌ DEPURACIÓN FALLÓ - Backend no pudo iniciar"
        log_debug "📋 Logs completos guardados en /app/debug/"
        exit 1
    fi
}

# Capturar señales
trap 'log_debug "🛑 Recibida señal de terminación"; exit 0' SIGTERM SIGINT

# Ejecutar función principal
main 