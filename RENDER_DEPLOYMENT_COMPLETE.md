# 🚀 Guía Completa de Despliegue en Render.com

## 📋 **Resumen del Proyecto**

Tu proyecto **Crypto AI Bot** es una aplicación compleja con múltiples servicios:
- **Backend FastAPI** (Python) - API principal con seguridad integral
- **AI Module** - Servicio de inteligencia artificial
- **Data Service** - Servicio de datos externos
- **Telegram Bot** - Bot de Telegram
- **Webapp** - Interfaz web (Next.js)

## 🎯 **Estrategia de Despliegue**

Para Render, vamos a desplegar **solo el Backend** inicialmente, ya que:
1. Es el servicio más crítico
2. Tiene toda la seguridad implementada
3. Funciona independientemente
4. Es más fácil de configurar

## ✅ **Preparación Completada**

### **Archivos Configurados:**
- ✅ `render.yaml` - Configuración de Render
- ✅ `src/backend/core/db.py` - Base de datos con variables de entorno
- ✅ `src/backend/core/config/security_config.py` - CORS actualizado
- ✅ `scripts/verify-render-setup.py` - Script de verificación

### **Verificación Local:**
```bash
python scripts/verify-render-setup.py
```

## 🚀 **Paso 1: Crear Cuenta en Render**

1. **Ir a [render.com](https://render.com)**
2. **Crear cuenta gratuita** (GitHub OAuth recomendado)
3. **Verificar email**

## 🔧 **Paso 2: Conectar Repositorio**

1. **En Render Dashboard:**
   - Click en "New +"
   - Seleccionar "Web Service"
   - Conectar cuenta de GitHub
   - Seleccionar repositorio `crypto-ai-bot`

## ⚙️ **Paso 3: Configurar Variables de Entorno**

### **Variables Críticas (Obligatorias):**

```bash
# Configuración básica
PYTHON_VERSION=3.11
BACKEND_PORT=8000
ENVIRONMENT=production
ENABLE_DOCS=false

# Base de datos (Render Postgres)
DATABASE_URL=postgresql://username:password@host:5432/database

# Seguridad
BACKEND_API_SECRET_KEY=tu_api_secret_key_super_segura_aqui
SECRET_KEY=tu_secret_key_super_segura_aqui

# CORS y Hosts
BACKEND_ALLOWED_ORIGINS=https://tu-app.onrender.com,http://localhost:3000
BACKEND_ALLOWED_HOSTS=tu-app.onrender.com,localhost,127.0.0.1

# Rate Limiting
BACKEND_RATE_LIMIT_PER_MINUTE=60
BACKEND_RATE_LIMIT_PER_HOUR=1000
BACKEND_RATE_LIMIT_PER_DAY=10000
```

### **Variables Opcionales (APIs Externas):**

```bash
# APIs de trading (opcional)
BINANCE_API_KEY=tu_binance_api_key
BINANCE_SECRET_KEY=tu_binance_secret_key
BINANCE_TESTNET=true

# APIs de datos (opcional)
ALPHA_VANTAGE_API_KEY=tu_alpha_vantage_key
NEWS_API_KEY=tu_news_api_key

# Telegram (opcional)
TELEGRAM_BOT_TOKEN=tu_telegram_bot_token
TELEGRAM_CHAT_ID=tu_chat_id

# OpenAI (opcional)
OPENAI_API_KEY=tu_openai_api_key
```

## 🗄️ **Paso 4: Configurar Base de Datos**

### **Opción A: Base de Datos Externa (Recomendado)**
1. **Crear base de datos PostgreSQL** en:
   - [Supabase](https://supabase.com) (Gratis)
   - [Neon](https://neon.tech) (Gratis)
   - [Railway](https://railway.app) (Gratis) - Alternativa

2. **Obtener DATABASE_URL** y configurarla en Render

### **Opción B: Render Postgres (Pago)**
1. **Crear PostgreSQL en Render**
2. **Conectar automáticamente** al Web Service

## 🔍 **Paso 5: Verificar Configuración**

### **Antes del Deploy:**
```bash
# Ejecutar verificación local
python scripts/verify-render-setup.py
```

### **Verificar que todos los archivos existen:**
- ✅ `src/backend/main_secure.py`
- ✅ `src/backend/core/db.py`
- ✅ `src/backend/core/config/security_config.py`
- ✅ `requirements/common.txt`
- ✅ `render.yaml`

## 🚀 **Paso 6: Deploy Automático**

1. **Render detectará automáticamente:**
   - ✅ Python 3.11
   - ✅ FastAPI en `src/backend/main_secure.py`
   - ✅ Endpoint `/ping` para healthcheck
   - ✅ `requirements/common.txt` para dependencias

2. **Build automático:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements/common.txt
   ```

3. **Start automático:**
   ```bash
   cd src/backend
   python main_secure.py
   ```

## ✅ **Paso 7: Verificar Deploy**

### **Logs Esperados:**
```
🚀 Iniciando Backend Securizado
📊 Configuración de seguridad: Rate Limiting 60/min
INFO:     Started server process [1]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### **Healthcheck:**
- ✅ Debería pasar en el primer intento
- ✅ Endpoint `/ping` respondiendo
- ✅ SSL automático configurado

### **Endpoints Disponibles:**
- ✅ `GET /ping` - Healthcheck simple
- ✅ `GET /health` - Health detallado
- ✅ `GET /healthcheck` - Health alternativo
- ✅ `GET /` - Información del servicio
- ✅ `GET /docs` - Documentación (si ENABLE_DOCS=true)

## 🔗 **Paso 8: URLs y Dominios**

### **URL Automática:**
```
https://tu-app.onrender.com
```

### **Endpoints de Prueba:**
```bash
# Healthcheck
curl https://tu-app.onrender.com/ping

# Información del servicio
curl https://tu-app.onrender.com/

# Health detallado
curl https://tu-app.onrender.com/health
```

## 📊 **Paso 9: Monitoreo**

### **En Render Dashboard:**
- ✅ **Logs en tiempo real**
- ✅ **Métricas de rendimiento**
- ✅ **Estado del servicio**
- ✅ **Deploy automático desde GitHub**

### **Alertas Configuradas:**
- ✅ **Deploy fallido**
- ✅ **Healthcheck fallido**
- ✅ **Error en logs**

## 🚨 **Solución de Problemas**

### **Si el Deploy Falla:**

1. **Verificar logs en Render Dashboard**
2. **Confirmar variables de entorno**
3. **Verificar que `main_secure.py` existe**
4. **Confirmar que `/ping` endpoint funciona**

### **Si Healthcheck Falla:**

1. **Verificar que puerto 8000 está expuesto**
2. **Confirmar que backend inicia correctamente**
3. **Verificar logs de uvicorn**
4. **Comprobar que DATABASE_URL es válida**

### **Si Dependencias Faltan:**

1. **Verificar `requirements/common.txt`**
2. **Confirmar que pip install funciona**
3. **Verificar versión de Python**

### **Si Base de Datos Falla:**

1. **Verificar DATABASE_URL**
2. **Confirmar que la base de datos está activa**
3. **Verificar credenciales**
4. **Comprobar conectividad desde Render**

## 🎯 **Próximos Pasos (Después del Backend)**

Una vez que el backend esté funcionando, puedes:

1. **Desplegar el AI Module** como servicio separado
2. **Desplegar el Data Service** como servicio separado
3. **Desplegar el Telegram Bot** como servicio separado
4. **Desplegar la Webapp** como servicio estático

## 🎉 **¡Despliegue Completado!**

**Tu backend estará disponible en:**
```
https://tu-app.onrender.com
```

**Con endpoints funcionales:**
- ✅ Healthcheck: `/ping`
- ✅ API principal: `/`
- ✅ Documentación: `/docs` (si habilitada)
- ✅ Seguridad integral implementada
- ✅ Rate limiting activo
- ✅ CORS configurado
- ✅ SSL automático

## 📞 **Soporte**

Si tienes problemas:
1. **Revisar logs en Render Dashboard**
2. **Ejecutar script de verificación local**
3. **Verificar variables de entorno**
4. **Comprobar conectividad de base de datos** 