# 🚂 Railway Troubleshooting Guide

## Problemas Comunes y Soluciones

### ❌ Healthcheck Falla

**Síntoma:** Railway muestra "service unavailable" en el healthcheck

**Soluciones:**

1. **Verificar endpoint de healthcheck:**
   ```bash
   # El endpoint debe responder inmediatamente
   curl http://localhost:8000/railway-health
   ```

2. **Verificar configuración en railway.toml:**
   ```toml
   [deploy]
   healthcheckPath = "/railway-health"
   healthcheckTimeout = 1800
   ```

3. **Verificar que el servicio esté iniciando correctamente:**
   - Revisar logs en Railway Dashboard
   - Verificar que `start.sh` esté ejecutándose
   - Confirmar que uvicorn esté corriendo en puerto 8000

### ❌ Servicio No Inicia

**Síntoma:** El contenedor se reinicia constantemente

**Soluciones:**

1. **Verificar variables de entorno:**
   ```bash
   # Variables obligatorias en Railway Dashboard
   BACKEND_PORT=8000
   ENVIRONMENT=production
   ```

2. **Verificar archivos de configuración:**
   - `start.sh` debe ser ejecutable
   - `main_secure.py` debe existir en `src/backend/`
   - Dependencias deben estar instaladas

3. **Verificar logs de inicio:**
   ```bash
   # En Railway Dashboard → Deployments → Latest → View Logs
   # Buscar errores específicos
   ```

### ❌ Dependencias No Se Instalan

**Síntoma:** Error durante el build

**Soluciones:**

1. **Verificar requirements/common.txt:**
   - Asegurar que todas las dependencias estén listadas
   - Verificar versiones compatibles

2. **Verificar Dockerfile:**
   - Confirmar que `requirements/common.txt` se copie correctamente
   - Verificar que pip install se ejecute sin errores

### ❌ Puerto No Disponible

**Síntoma:** Error de conexión al puerto

**Soluciones:**

1. **Verificar configuración de puertos:**
   ```toml
   [[services]]
   name = "crypto-ai-bot"
   port = 8000
   ```

2. **Verificar que uvicorn esté configurado correctamente:**
   ```bash
   uvicorn main_secure:app --host 0.0.0.0 --port 8000
   ```

## 🔧 Comandos de Diagnóstico

### Probar Endpoints Localmente

```bash
# Probar healthcheck
curl http://localhost:8000/railway-health

# Probar endpoint principal
curl http://localhost:8000/health

# Probar endpoint de prueba
curl http://localhost:8000/test
```

### Verificar Logs

```bash
# En Railway Dashboard
# Deployments → Latest → View Logs

# Buscar patrones específicos:
# - "Started server process"
# - "Uvicorn running on"
# - "Healthcheck endpoint llamado"
```

### Verificar Configuración

```bash
# Verificar archivos de configuración
ls -la railway.toml
ls -la start.sh
ls -la src/backend/main_secure.py

# Verificar permisos
chmod +x start.sh
```

## 📊 Monitoreo

### Métricas a Observar

1. **CPU Usage:** Debe estar por debajo del 80%
2. **Memory Usage:** Debe estar por debajo del 80%
3. **Response Time:** Healthcheck debe responder en < 1s
4. **Error Rate:** Debe ser 0% para endpoints de healthcheck

### Alertas Configuradas

- Healthcheck falla por más de 5 minutos
- CPU > 90% por más de 10 minutos
- Memory > 90% por más de 10 minutos
- Error rate > 5% en endpoints críticos

## 🚀 Optimizaciones para Railway

### Configuración Recomendada

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

### Variables de Entorno

```bash
# Obligatorias
BACKEND_PORT=8000
ENVIRONMENT=production

# Opcionales
ENABLE_DOCS=false
LOG_LEVEL=info
```

### Configuración de Uvicorn

```bash
uvicorn main_secure:app --host 0.0.0.0 --port 8000 --workers 1 --log-level info
```

## 📞 Soporte

Si los problemas persisten:

1. **Revisar logs completos** en Railway Dashboard
2. **Verificar configuración** de variables de entorno
3. **Probar endpoints** manualmente
4. **Contactar soporte** de Railway si es necesario

## 🔄 Rollback

En caso de problemas críticos:

1. **Railway Dashboard → Deployments**
2. **Seleccionar versión anterior estable**
3. **Click en "Redeploy"**
4. **Verificar que funcione correctamente** 