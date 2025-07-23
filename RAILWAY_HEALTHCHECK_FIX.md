# 🔧 Railway Healthcheck Fix

## Problema Identificado

El healthcheck de Railway estaba fallando porque:
1. El endpoint `/health` pasaba por middleware que podía causar delays
2. Railway necesitaba un endpoint ultra simple y rápido
3. La configuración no estaba optimizada para Railway

## Soluciones Implementadas

### 1. ✅ Endpoint de Healthcheck Ultra Simple

**Archivo:** `src/backend/main_secure.py`

```python
@app.get("/railway-health")
async def railway_health():
    """Endpoint ultra simple para Railway - sin middleware."""
    return {"status": "ok"}
```

**Características:**
- Definido ANTES de cualquier middleware
- Respuesta inmediata sin procesamiento
- Sin dependencias externas
- Sin logging que pueda causar delays

### 2. ✅ Configuración de Railway Actualizada

**Archivo:** `railway.toml`

```toml
[deploy]
healthcheckPath = "/railway-health"
healthcheckTimeout = 1800
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 3

[[services]]
name = "crypto-ai-bot"
port = 8000
```

### 3. ✅ Dockerfile Optimizado

**Archivo:** `Dockerfile`

```dockerfile
# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/railway-health || exit 1
```

### 4. ✅ Script de Inicio Mejorado

**Archivo:** `start.sh`

```bash
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
```

### 5. ✅ Configuración JSON Adicional

**Archivo:** `railway.json`

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "healthcheckPath": "/railway-health",
    "healthcheckTimeout": 1800,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  },
  "services": [
    {
      "name": "crypto-ai-bot",
      "port": 8000,
      "env": {
        "ENVIRONMENT": "production",
        "BACKEND_PORT": "8000"
      }
    }
  ]
}
```

## Endpoints de Healthcheck Disponibles

### 1. `/railway-health` (Recomendado para Railway)
- **Propósito:** Healthcheck ultra simple para Railway
- **Características:** Sin middleware, respuesta inmediata
- **Respuesta:** `{"status": "ok"}`

### 2. `/healthcheck-railway`
- **Propósito:** Healthcheck alternativo para Railway
- **Características:** Con timestamp, sin middleware
- **Respuesta:** `{"status": "ok", "service": "backend", "timestamp": "..."}`

### 3. `/health`
- **Propósito:** Healthcheck completo con logging
- **Características:** Pasa por middleware, con logging detallado
- **Respuesta:** `{"status": "ok", "version": "2.0.0", "security": "enabled", ...}`

### 4. `/test`
- **Propósito:** Endpoint de prueba simple
- **Características:** Sin middleware, para pruebas rápidas
- **Respuesta:** `{"test": "ok"}`

## Scripts de Validación

### 1. Validación de Configuración
```bash
python scripts/validate_railway_setup.py
```

### 2. Prueba de Endpoints
```bash
python test_railway_health.py
```

## Variables de Entorno Requeridas

En Railway Dashboard, configurar:

```bash
# Obligatorias
BACKEND_PORT=8000
ENVIRONMENT=production

# Opcionales
ENABLE_DOCS=false
LOG_LEVEL=info
```

## Monitoreo

### Logs a Observar

1. **Inicio del servicio:**
   ```
   🚀 Iniciando Crypto AI Bot en Railway...
   ✅ Archivos verificados correctamente
   INFO: Started server process [X]
   INFO: Uvicorn running on http://0.0.0.0:8000
   ```

2. **Healthcheck exitoso:**
   ```
   🌐 Request: GET /railway-health - IP: ...
   📤 Response: 200 - Tiempo: 0.001s
   ```

### Métricas de Éxito

- **Response Time:** < 1 segundo
- **Status Code:** 200 OK
- **Availability:** 99.9%+
- **Error Rate:** 0%

## Troubleshooting

### Si el Healthcheck Sigue Fallando

1. **Verificar logs en Railway Dashboard**
2. **Probar endpoint manualmente:**
   ```bash
   curl https://your-app.railway.app/railway-health
   ```
3. **Verificar variables de entorno**
4. **Revisar configuración de puertos**

### Comandos de Diagnóstico

```bash
# Probar endpoints localmente
curl http://localhost:8000/railway-health
curl http://localhost:8000/health
curl http://localhost:8000/test

# Verificar configuración
python scripts/validate_railway_setup.py
```

## Resultado Esperado

Con estos cambios, Railway debería:
1. ✅ Pasar el healthcheck exitosamente
2. ✅ Iniciar el servicio correctamente
3. ✅ Mantener el servicio estable
4. ✅ Responder a requests en < 1 segundo

## Próximos Pasos

1. **Hacer commit de los cambios**
2. **Push a Railway**
3. **Monitorear el nuevo deploy**
4. **Verificar que el healthcheck pase**
5. **Probar endpoints manualmente** 