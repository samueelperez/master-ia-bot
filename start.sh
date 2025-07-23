#!/bin/bash
set -e

echo "🚀 Iniciando Crypto AI Bot en Railway..."

# Crear directorios necesarios
mkdir -p /app/logs /app/pids

# Verificar que estamos en el directorio correcto
cd /app

# Verificar que el archivo main_secure.py existe
if [ ! -f "src/backend/main_secure.py" ]; then
    echo "❌ Error: main_secure.py no encontrado"
    exit 1
fi

echo "✅ Archivos verificados correctamente"

# Lanzar el backend con configuración optimizada para Railway
cd src/backend && uvicorn main_secure:app --host 0.0.0.0 --port 8000 --workers 1 --log-level info 