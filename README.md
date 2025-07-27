# 🤖 Crypto AI Bot - Bot de Trading Inteligente

Un bot de trading de criptomonedas impulsado por IA que combina análisis técnico, noticias y sentimiento del mercado para generar señales de trading.

## 🚀 Características Principales

- **Análisis Multi-Timeframe**: Análisis técnico en múltiples timeframes
- **IA Avanzada**: Integración con modelos de lenguaje para análisis de mercado
- **Noticias en Tiempo Real**: Análisis de noticias y eventos económicos
- **Señales de Trading**: Generación automática de señales de compra/venta
- **Bot de Telegram**: Interfaz conversacional para consultas y alertas
- **Webapp**: Dashboard web para monitoreo y configuración
- **Despliegue en Render**: Configuración lista para producción

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram Bot  │    │   AI Module     │    │    Backend      │
│   (Node.js)     │◄──►│   (Python)      │◄──►│   (Python)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│  Data Service   │◄─────────────┘
                        │   (Python)      │
                        └─────────────────┘
                                │
                        ┌─────────────────┐
                        │    Webapp       │
                        │   (Next.js)     │
                        └─────────────────┘
```

## 📋 Componentes

### 🤖 **AI Module** (`src/ai-module/`)
- Análisis de mercado con IA
- Generación de señales de trading
- Integración con modelos de lenguaje
- Estrategias avanzadas de trading

### 🔧 **Backend** (`src/backend/`)
- API REST para gestión de datos
- Procesamiento de indicadores técnicos
- Gestión de estrategias de trading
- Sistema de autenticación y seguridad

### 📱 **Telegram Bot** (`src/telegram-bot/`)
- Interfaz conversacional
- Consultas de mercado en tiempo real
- Alertas y notificaciones
- Gestión de usuarios

### 📊 **Data Service** (`src/data-service/`)
- Integración con APIs externas
- Caché de datos de mercado
- Servicios de noticias y eventos
- Análisis de sentimiento social

### 🌐 **Webapp** (`src/webapp/`)
- Dashboard web interactivo
- Gráficos técnicos en tiempo real
- Configuración de estrategias
- Monitoreo de rendimiento

## 🛠️ Instalación Local

### Prerrequisitos

- Python 3.8+
- Node.js 16+
- Docker y Docker Compose
- Git

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/master-ia-bot-final.git
cd master-ia-bot-final
```

### 2. Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp config/env.example .env

# Editar con tus credenciales reales
nano .env
```

### 3. Instalar Dependencias

```bash
# Python dependencies
pip install -r requirements/ai-module.txt
pip install -r requirements/backend.txt
pip install -r requirements/data-service.txt

# Node.js dependencies (webapp)
cd src/webapp
npm install
cd ../..
```

### 4. Configurar Base de Datos

```bash
# PostgreSQL (recomendado para producción)
# O usar SQLite para desarrollo
```

### 5. Iniciar Servicios

```bash
# Usando Docker Compose (recomendado)
docker-compose up -d

# O manualmente
python src/ai-module/main.py &
python src/backend/main.py &
python src/data-service/main.py &
cd src/webapp && npm run dev &
```

## 🚀 Despliegue en Render

### 1. Preparar el Repositorio

```bash
# Asegúrate de que todos los archivos estén committeados
git add .
git commit -m "🚀 Preparando para despliegue en Render"
git push origin main
```

### 2. Crear Proyecto en Render

1. Ve a [Render.com](https://render.com)
2. Crea una nueva cuenta o inicia sesión
3. Haz clic en "New Project"
4. Selecciona "Deploy from GitHub repo"
5. Conecta tu repositorio de GitHub

### 3. Configurar Variables de Entorno

En Render, ve a la pestaña "Environment" y configura todas las variables de `config/env.example` con tus valores reales.

### 4. Desplegar

Render detectará automáticamente la configuración y desplegará tu aplicación.

**📖 Para instrucciones detalladas, consulta [RENDER_DEPLOYMENT_COMPLETE.md](RENDER_DEPLOYMENT_COMPLETE.md)**

## 🔐 Seguridad

### Variables de Entorno Críticas

**NUNCA** subas estos archivos al repositorio:
- `.env`
- `config/.env*`
- `*secrets*`
- `*secret*`

### Configuración de Seguridad

El proyecto incluye:
- Autenticación JWT

- Validación de entrada
- Cifrado de datos sensibles
- Middleware de seguridad

## 📊 Uso

### Telegram Bot

1. Inicia el bot: `/start`
2. Consulta mercado: `/market BTC`
3. Análisis técnico: `/analysis ETH 1h`
4. Configurar alertas: `/alerts`

### Webapp

1. Abre `http://localhost:3000`
2. Inicia sesión con tus credenciales
3. Configura tus estrategias
4. Monitorea el rendimiento

### API

```bash
# Análisis de mercado
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT", "timeframe": "1h"}'

# Señales de trading
curl -X GET http://localhost:8000/signals/BTCUSDT
```

## 🧪 Testing

```bash
# Tests unitarios
python -m pytest tests/unit/

# Tests de integración
python -m pytest tests/integration/

# Tests completos
python -m pytest tests/
```

## 📈 Monitoreo

- **Logs**: Revisa `logs/` para debugging
- **Métricas**: Dashboard en la webapp
- **Alertas**: Notificaciones en Telegram
- **Health Checks**: Endpoints `/health` en cada servicio

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## ⚠️ Disclaimer

Este bot es para fines educativos y de investigación. El trading de criptomonedas conlleva riesgos significativos. No inviertas más de lo que puedas permitirte perder.

## 🆘 Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/master-ia-bot-final/issues)
- **Documentación**: [Wiki del proyecto](https://github.com/tu-usuario/master-ia-bot-final/wiki)
- **Telegram**: @tu_bot_username

---

**¡Happy Trading! 🚀📈**
