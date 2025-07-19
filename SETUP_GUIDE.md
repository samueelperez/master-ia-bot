# 🚀 Guía de Configuración - Crypto AI Bot

## 📋 Pasos para Configurar el Proyecto

### 1. **Clonar el Repositorio**

```bash
git clone https://github.com/tu-usuario/master-ia-bot-final.git
cd master-ia-bot-final
```

### 2. **Configurar Variables de Entorno**

```bash
# Copiar el archivo de ejemplo
cp config/env.example .env

# Editar con tus credenciales reales
nano .env
```

### 3. **Variables de Entorno Requeridas**

#### 🔑 **API Keys Obligatorias**
```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=tu_token_de_telegram_aqui
TELEGRAM_CHAT_ID=tu_chat_id_de_telegram_aqui

# OpenAI / LLM
OPENAI_API_KEY=tu_openai_api_key_aqui
HUGGINGFACE_API_KEY=tu_huggingface_token_aqui

# Base de Datos
DATABASE_URL=postgresql://usuario:password@localhost:5432/crypto_ai_bot
REDIS_URL=redis://localhost:6379/0
```

#### 🔧 **Configuración de Seguridad**
```bash
# Claves de seguridad (generar con: openssl rand -hex 32)
JWT_SECRET_KEY=tu_jwt_secret_key_aqui
ENCRYPTION_KEY=tu_encryption_key_aqui
ADMIN_USER_ID=tu_user_id_de_telegram_aqui
```

#### 📊 **APIs Externas (Opcionales)**
```bash
# Trading
BINANCE_API_KEY=tu_binance_api_key_aqui
BINANCE_SECRET_KEY=tu_binance_secret_key_aqui

# Noticias y Datos
ALPHA_VANTAGE_API_KEY=tu_alpha_vantage_key_aqui
NEWS_API_KEY=tu_news_api_key_aqui
TWITTER_BEARER_TOKEN=tu_twitter_token_aqui
```

### 4. **Instalar Dependencias**

#### Python
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements/ai-module.txt
pip install -r requirements/backend.txt
pip install -r requirements/data-service.txt
```

#### Node.js (Webapp)
```bash
cd src/webapp
npm install
cd ../..
```

### 5. **Configurar Base de Datos**

#### Opción A: PostgreSQL (Recomendado)
```bash
# Instalar PostgreSQL
# En macOS: brew install postgresql
# En Ubuntu: sudo apt-get install postgresql

# Crear base de datos
createdb crypto_ai_bot
```

#### Opción B: SQLite (Desarrollo)
```bash
# SQLite se creará automáticamente
# No requiere configuración adicional
```

### 6. **Iniciar Servicios**

#### Opción A: Docker Compose (Recomendado)
```bash
docker-compose up -d
```

#### Opción B: Manual
```bash
# Terminal 1: AI Module
python src/ai-module/main.py

# Terminal 2: Backend
python src/backend/main.py

# Terminal 3: Data Service
python src/data-service/main.py

# Terminal 4: Telegram Bot
python src/telegram-bot/core/telegram_bot_secure.py

# Terminal 5: Webapp
cd src/webapp && npm run dev
```

## 🚀 Despliegue en Railway

### 1. **Preparar el Repositorio**
```bash
git add .
git commit -m "🚀 Configuración inicial lista"
git push origin main
```

### 2. **Crear Proyecto en Railway**
1. Ve a [Railway.app](https://railway.app)
2. Crea cuenta o inicia sesión
3. Haz clic en "New Project"
4. Selecciona "Deploy from GitHub repo"
5. Conecta tu repositorio

### 3. **Configurar Variables de Entorno en Railway**
En Railway, ve a la pestaña "Variables" y configura todas las variables de `config/env.example` con tus valores reales.

### 4. **Desplegar**
Railway detectará automáticamente la configuración y desplegará tu aplicación.

**📖 Para instrucciones detalladas, consulta [RAILWAY_DEPLOYMENT_GUIDE.md](RAILWAY_DEPLOYMENT_GUIDE.md)**

## 🔐 Seguridad

### ✅ **Buenas Prácticas**
- **NUNCA** subas archivos `.env` al repositorio
- Usa variables de entorno para todas las credenciales
- Genera claves de seguridad únicas para cada entorno
- Revisa regularmente los logs de seguridad

### ❌ **Qué NO Hacer**
- No hardcodear credenciales en el código
- No subir archivos de configuración con secretos
- No usar las mismas claves en desarrollo y producción
- No compartir tokens de API públicamente

## 🧪 Testing

### Verificar Instalación
```bash
# Test de conectividad
python -c "import requests; print('✅ Requests instalado')"

# Test de base de datos
python -c "import sqlite3; print('✅ SQLite funcionando')"

# Test de Telegram
python -c "import telegram; print('✅ Telegram instalado')"
```

### Tests Automatizados
```bash
# Tests unitarios
python -m pytest tests/unit/

# Tests de integración
python -m pytest tests/integration/

# Tests completos
python -m pytest tests/
```

## 📊 Monitoreo

### Logs
```bash
# Ver logs en tiempo real
tail -f logs/ai-module.log
tail -f logs/backend.log
tail -f logs/telegram-bot.log
```

### Health Checks
```bash
# Verificar estado de servicios
curl http://localhost:8001/health  # AI Module
curl http://localhost:8000/health  # Backend
curl http://localhost:8002/health  # Data Service
```

## 🆘 Solución de Problemas

### Error: "Module not found"
```bash
# Verificar instalación de dependencias
pip list | grep nombre_del_modulo
pip install -r requirements/nombre_del_modulo.txt
```

### Error: "Database connection failed"
```bash
# Verificar configuración de base de datos
echo $DATABASE_URL
# Asegúrate de que la base de datos esté creada y accesible
```

### Error: "Telegram bot not responding"
```bash
# Verificar token de Telegram
echo $TELEGRAM_BOT_TOKEN
# Asegúrate de que el bot esté creado en @BotFather
```

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/master-ia-bot-final/issues)
- **Documentación**: [Wiki del proyecto](https://github.com/tu-usuario/master-ia-bot-final/wiki)
- **Telegram**: @tu_bot_username

---

**¡Configuración Completada! 🎉** 