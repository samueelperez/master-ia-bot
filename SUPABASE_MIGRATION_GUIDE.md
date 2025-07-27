# 🚀 Guía de Migración a Supabase - Crypto AI Bot

## 📋 Resumen

Esta guía te ayudará a migrar completamente el proyecto Crypto AI Bot de SQLite/PostgreSQL local a Supabase.

## 🔧 Configuración Inicial

### 1. Variables de Entorno

Agrega las siguientes variables a tu archivo `.env`:

```bash
# ========================================
# SUPABASE CONFIGURATION
# ========================================
SUPABASE_URL=https://baotpqenzaicldzgeinu.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJhb3RwcWVuemFpY2xkemdlaW51Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM2NDA3MjAsImV4cCI6MjA2OTIxNjcyMH0.bZbFYJgGOdPzVvTDQoo-CTDc0r8PMCfAunv3s3TlcZ4
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
SUPABASE_DB_PASSWORD=your_database_password_here
```

### 2. Instalar Dependencias

```bash
pip install supabase==2.3.4
```

## 🗄️ Configuración de la Base de Datos

### 1. Ejecutar Script SQL

1. Ve al **SQL Editor** en tu dashboard de Supabase
2. Copia y pega todo el contenido del archivo `supabase_setup.sql`
3. Ejecuta el script completo

### 2. Verificar Tablas Creadas

Después de ejecutar el script, deberías ver estas tablas:

- ✅ `telegram_users` - Usuarios del bot
- ✅ `suggestions` - Sugerencias de usuarios
- ✅ `alerts` - Alertas de precio
- ✅ `user_configurations` - Configuraciones de usuario
- ✅ `activity_logs` - Logs de actividad
- ✅ `technical_analyses` - Análisis técnicos
- ✅ `trading_signals` - Señales de trading

## 🔄 Migración de Datos

### 1. Migrar Sugerencias Existentes

Si tienes sugerencias en SQLite, puedes migrarlas con este script:

```python
import sqlite3
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

# Conectar a SQLite
sqlite_conn = sqlite3.connect('suggestions.db')
sqlite_cursor = sqlite_conn.cursor()

# Conectar a Supabase
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_ANON_KEY')
)

# Obtener sugerencias de SQLite
sqlite_cursor.execute('SELECT * FROM suggestions')
suggestions = sqlite_cursor.fetchall()

# Migrar a Supabase
for suggestion in suggestions:
    supabase.table('suggestions').insert({
        'user_id': suggestion[1],
        'suggestion_text': suggestion[2],
        'user_info': suggestion[3] if suggestion[3] else {},
        'status': suggestion[4],
        'admin_notes': suggestion[5],
        'created_at': suggestion[6],
        'updated_at': suggestion[7]
    }).execute()

print(f"✅ Migradas {len(suggestions)} sugerencias")
```

## 🛠️ Actualización del Código

### 1. Backend - Servicio de Sugerencias

Reemplaza `src/backend/services/suggestions/suggestions.py`:

```python
from core.supabase_config import supabase_service

class SuggestionsService:
    def __init__(self):
        self.supabase = supabase_service
    
    def add_suggestion(self, user_id: str, suggestion_text: str, user_info: dict = None):
        try:
            result = self.supabase.create_suggestion(
                user_id=int(user_id),
                suggestion_text=suggestion_text,
                user_info=user_info
            )
            return {
                "status": "success",
                "id": result['id'],
                "message": "Sugerencia creada exitosamente"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_suggestions(self, limit: int = 50, status: str = None):
        try:
            suggestions = self.supabase.get_suggestions(limit=limit, status=status)
            return suggestions
        except Exception as e:
            return []
```

### 2. Telegram Bot - Gestión de Usuarios

Actualiza `src/telegram-bot/core/telegram_bot_secure.py`:

```python
from core.supabase_config import supabase_service

# En la función process_message
async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    
    # Crear/actualizar usuario en Supabase
    try:
        supabase_service.create_or_update_user(
            telegram_id=user_id,
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name
        )
    except Exception as e:
        logger.error(f"Error actualizando usuario en Supabase: {e}")
```

## 🔐 Configuración de Seguridad

### 1. Row Level Security (RLS)

Las políticas RLS ya están configuradas en el script SQL. Verifica que estén activas:

```sql
-- Verificar políticas RLS
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual 
FROM pg_policies 
WHERE schemaname = 'public';
```

### 2. Service Role Key

Para operaciones administrativas, necesitas la Service Role Key:

1. Ve a **Settings > API** en Supabase
2. Copia la **service_role** key
3. Agrégala a tu `.env` como `SUPABASE_SERVICE_ROLE_KEY`

## 📊 Monitoreo y Estadísticas

### 1. Dashboard de Supabase

Puedes monitorear el uso desde el dashboard de Supabase:

- **Table Editor**: Ver datos en tiempo real
- **Logs**: Monitorear consultas y errores
- **API**: Ver uso de la API

### 2. Vistas Útiles

El script SQL crea estas vistas útiles:

```sql
-- Estadísticas de sugerencias
SELECT * FROM suggestions_stats;

-- Estadísticas de usuarios activos
SELECT * FROM active_users_stats;
```

## 🚀 Despliegue

### 1. Variables de Entorno en Producción

Asegúrate de configurar estas variables en tu entorno de producción:

```bash
SUPABASE_URL=https://baotpqenzaicldzgeinu.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

### 2. Verificar Conexión

Agrega este código para verificar la conexión:

```python
from core.supabase_config import supabase_service

# Verificar conexión
if supabase_service.config.test_connection():
    print("✅ Conexión a Supabase exitosa")
else:
    print("❌ Error conectando a Supabase")
```

## 🔍 Troubleshooting

### Problemas Comunes

1. **Error de conexión**:
   - Verifica las credenciales de Supabase
   - Asegúrate de que la URL sea correcta

2. **Error de permisos**:
   - Verifica que las políticas RLS estén configuradas
   - Usa la service role key para operaciones administrativas

3. **Error de dependencias**:
   - Instala `supabase==2.3.4`
   - Verifica que Python sea 3.8+

### Logs Útiles

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## ✅ Checklist de Migración

- [ ] Variables de entorno configuradas
- [ ] Script SQL ejecutado en Supabase
- [ ] Dependencias instaladas
- [ ] Código actualizado para usar Supabase
- [ ] Datos migrados (si aplica)
- [ ] Conexión verificada
- [ ] Políticas RLS activas
- [ ] Service role key configurada
- [ ] Pruebas realizadas

## 🎯 Beneficios de Supabase

- ✅ **Escalabilidad**: Maneja millones de usuarios
- ✅ **Seguridad**: RLS y autenticación integrada
- ✅ **Real-time**: Suscripciones en tiempo real
- ✅ **Backup automático**: Sin preocupaciones de datos
- ✅ **Dashboard**: Monitoreo visual
- ✅ **API REST**: Fácil integración

¡Tu proyecto ahora está completamente migrado a Supabase! 🚀 