#!/bin/bash

# Script de despliegue automatizado para Render.com
set -e

echo "🚀 DESPLIEGUE AUTOMATIZADO EN RENDER"
echo "===================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "render.yaml" ]; then
    error "No se encontró render.yaml. Asegúrate de estar en el directorio raíz del proyecto."
    exit 1
fi

# Verificar que render CLI está instalado
if ! command -v render &> /dev/null; then
    error "Render CLI no está instalado. Instálalo con: brew install render"
    exit 1
fi

# Verificar autenticación
log "Verificando autenticación con Render..."
if ! render whoami &> /dev/null; then
    error "No estás autenticado con Render. Ejecuta: render login"
    exit 1
fi

success "Autenticación verificada"

# Verificar que git está configurado
log "Verificando configuración de Git..."
if [ -z "$(git config user.name)" ] || [ -z "$(git config user.email)" ]; then
    warning "Git no está configurado completamente"
    echo "Configura Git con:"
    echo "git config --global user.name 'Tu Nombre'"
    echo "git config --global user.email 'tu@email.com'"
    exit 1
fi

# Verificar que no hay cambios pendientes
log "Verificando cambios pendientes..."
if [ -n "$(git status --porcelain)" ]; then
    warning "Hay cambios pendientes en Git"
    echo "Cambios pendientes:"
    git status --short
    
    read -p "¿Quieres hacer commit de estos cambios? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log "Haciendo commit de cambios..."
        git add .
        git commit -m "🚀 Deploy automático en Render - $(date)"
    else
        error "Debes hacer commit de los cambios antes de continuar"
        exit 1
    fi
fi

# Push de cambios
log "Haciendo push de cambios..."
git push origin main
success "Cambios enviados a GitHub"

# Verificar si el proyecto ya existe
log "Verificando si el proyecto ya existe..."
PROJECT_NAME="crypto-ai-bot"
PROJECT_EXISTS=false

if render projects list --output json | grep -q "\"name\":\"$PROJECT_NAME\""; then
    PROJECT_EXISTS=true
    success "Proyecto $PROJECT_NAME ya existe"
else
    log "Proyecto $PROJECT_NAME no existe, se creará"
fi

# Crear proyecto si no existe
if [ "$PROJECT_EXISTS" = false ]; then
    log "Creando proyecto $PROJECT_NAME..."
    echo "Nota: Este paso requiere interacción manual en el navegador"
    echo "1. Se abrirá el navegador"
    echo "2. Selecciona 'Create New Project'"
    echo "3. Elige 'From Git Repository'"
    echo "4. Conecta tu repositorio de GitHub"
    echo "5. Selecciona el repositorio: samueelperez/master-ia-bot"
    echo "6. En 'Environment', selecciona 'Python'"
    echo "7. En 'Build Command', usa: pip install -r requirements.txt"
    echo "8. En 'Start Command', usa: cd src/backend && python main_secure.py"
    echo "9. Haz clic en 'Create Web Service'"
    
    read -p "Presiona Enter cuando hayas completado estos pasos..."
fi

# Verificar que el servicio existe
log "Verificando servicios..."
SERVICES=$(render services list --output json 2>/dev/null || echo "[]")

if echo "$SERVICES" | grep -q "crypto-ai-bot-backend"; then
    success "Servicio crypto-ai-bot-backend encontrado"
else
    warning "Servicio crypto-ai-bot-backend no encontrado"
    echo "Asegúrate de que el servicio se haya creado correctamente en Render Dashboard"
fi

# Mostrar información del despliegue
log "Información del despliegue:"
echo "=========================="
echo "📁 Proyecto: $PROJECT_NAME"
echo "🔗 Repositorio: https://github.com/samueelperez/master-ia-bot"
echo "📋 Archivo de configuración: render.yaml"
echo "🐍 Python: 3.11"
echo "🚀 Build Command: pip install -r requirements.txt"
echo "▶️ Start Command: cd src/backend && python main_secure.py"
echo "🏥 Health Check: /ping"

# Verificar variables de entorno
log "Verificando variables de entorno..."
if [ -f "config/render.env.example" ]; then
    echo "📋 Variables de entorno disponibles en: config/render.env.example"
    echo "⚠️ IMPORTANTE: Configura estas variables en Render Dashboard:"
    echo "   - Ve a tu servicio en Render"
    echo "   - Click en 'Environment'"
    echo "   - Agrega las variables del archivo config/render.env.example"
else
    warning "Archivo de variables de entorno no encontrado"
fi

# Verificar base de datos
log "Verificando configuración de base de datos..."
echo "🗄️ Base de datos requerida:"
echo "   - Crea una cuenta en https://supabase.com (gratis)"
echo "   - Crea un nuevo proyecto PostgreSQL"
echo "   - Copia la DATABASE_URL"
echo "   - Configúrala en Render Dashboard"

success "Despliegue configurado correctamente!"
echo ""
echo "🎯 Próximos pasos:"
echo "1. Configura las variables de entorno en Render Dashboard"
echo "2. Configura la base de datos (Supabase/Neon)"
echo "3. El servicio se desplegará automáticamente"
echo "4. Verifica los logs en Render Dashboard"
echo ""
echo "🔗 URL del servicio: https://crypto-ai-bot-backend.onrender.com"
echo "📊 Dashboard: https://dashboard.render.com" 