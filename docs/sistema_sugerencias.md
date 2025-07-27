# 💡 Sistema de Sugerencias

## 📋 **Descripción General**

El sistema de sugerencias permite a los usuarios enviar feedback, reportar bugs, proponer mejoras y solicitar nuevas funcionalidades para el bot de Crypto AI. El sistema está completamente integrado con SQLite para el almacenamiento y incluye gestión administrativa.

## 🏗️ **Arquitectura**

### **Componentes Principales:**

1. **Backend API** (`src/backend/`)
   - `models/suggestion_models.py` - Modelos Pydantic
   - `services/suggestions.py` - Servicio de gestión
   - `main.py` - Endpoints REST

2. **Bot de Telegram** (`src/telegram-bot/`)
   - `core/telegram_bot_secure.py` - Comandos y callbacks
   - Integración con ConversationHandler

3. **Base de Datos**
   - `suggestions.db` - Base de datos SQLite separada
   - Tabla `suggestions` con constraints de seguridad

## 🗄️ **Estructura de la Base de Datos**

### **Tabla `suggestions`:**
```sql
CREATE TABLE suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL CHECK(user_id > 0),
    username TEXT CHECK(length(username) <= 100),
    first_name TEXT CHECK(length(first_name) <= 100),
    suggestion_text TEXT NOT NULL CHECK(length(suggestion_text) <= 2000),
    category TEXT CHECK(category IN ('improvement', 'bug', 'feature', 'feedback', 'general')) DEFAULT 'general',
    status TEXT CHECK(status IN ('pending', 'approved', 'rejected', 'in_progress')) DEFAULT 'pending',
    priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'urgent')) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    admin_notes TEXT CHECK(length(admin_notes) <= 1000),
    admin_id INTEGER
);
```

### **Tabla `users`:**
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY CHECK(user_id > 0),
    username TEXT CHECK(length(username) <= 100),
    first_name TEXT CHECK(length(first_name) <= 100),
    last_name TEXT CHECK(length(last_name) <= 100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 **API Endpoints**

### **1. Crear Sugerencia**
```http
POST /sugerencias
Content-Type: application/json

{
    "suggestion_text": "Me gustaría que agreguen más indicadores técnicos",
    "category": "improvement",
    "priority": "medium"
}
```

**Respuesta:**
```json
{
    "status": "success",
    "message": "Sugerencia creada exitosamente",
    "suggestion_id": 123
}
```

### **2. Listar Sugerencias**
```http
GET /sugerencias?limit=50&status=pending&category=bug
```

**Respuesta:**
```json
{
    "status": "success",
    "message": "Sugerencias obtenidas exitosamente",
    "suggestions": [...],
    "total_count": 25,
    "pending_count": 10,
    "approved_count": 12,
    "rejected_count": 3
}
```

### **3. Actualizar Estado**
```http
PUT /sugerencias/{suggestion_id}
Content-Type: application/json

{
    "status": "approved",
    "admin_notes": "Excelente sugerencia, será implementada",
    "admin_id": 12345
}
```

### **4. Estadísticas**
```http
GET /sugerencias/stats
```

**Respuesta:**
```json
{
    "status": "success",
    "message": "Estadísticas obtenidas exitosamente",
    "data": {
        "total_suggestions": 25,
        "pending_suggestions": 10,
        "approved_suggestions": 12,
        "rejected_suggestions": 3,
        "in_progress_suggestions": 0,
        "recent_suggestions": 5,
        "top_categories": {"improvement": 10, "bug": 8, "feature": 5},
        "top_priorities": {"medium": 15, "high": 7, "low": 3}
    }
}
```

### **5. Eliminar Sugerencia**
```http
DELETE /sugerencias/{suggestion_id}
```

### **6. Limpiar Sugerencias Antiguas**
```http
POST /sugerencias/cleanup?days_to_keep=365
```

## 🤖 **Comandos del Bot de Telegram**

### **Comando Principal:**
```
/sugerencias
```

### **Flujo de Usuario:**

1. **Enviar Sugerencia:**
   - Usuario ejecuta `/sugerencias`
   - Selecciona "💡 Enviar Sugerencia"
   - Escribe su sugerencia (mínimo 10 caracteres)
   - Recibe confirmación con ID

2. **Ver Mis Sugerencias:**
   - Usuario ejecuta `/sugerencias`
   - Selecciona "📋 Ver Mis Sugerencias"
   - Ve lista de sus sugerencias con estados

3. **Estadísticas (Solo Admins):**
   - Usuario ejecuta `/sugerencias`
   - Selecciona "📊 Estadísticas"
   - Ve estadísticas completas del sistema

### **Flujo de Administrador:**

1. **Acceso al Panel:**
   - Admin ejecuta `/admin`
   - Selecciona "💡 Gestionar Sugerencias"

2. **Gestión de Sugerencias:**
   - Ve sugerencias pendientes
   - Puede aprobar/rechazar con botones
   - Agrega notas administrativas

3. **Ver Todas las Sugerencias:**
   - Accede a estadísticas completas
   - Ve historial de todas las sugerencias

## 📊 **Categorías y Estados**

### **Categorías:**
- 🐛 **Bug** - Reporte de errores
- ✨ **Feature** - Nueva funcionalidad
- 🔧 **Improvement** - Mejora de funcionalidad existente
- 💭 **Feedback** - Comentarios generales
- 📝 **General** - Otros tipos

### **Estados:**
- ⏳ **Pending** - Pendiente de revisión
- ✅ **Approved** - Aprobada para implementación
- ❌ **Rejected** - Rechazada
- 🔄 **In Progress** - En desarrollo

### **Prioridades:**
- 🔴 **Urgent** - Crítica, requiere atención inmediata
- 🟡 **High** - Importante, prioridad alta
- 🟢 **Medium** - Normal, prioridad media
- ⚪ **Low** - Baja prioridad

## 🔒 **Seguridad y Validación**

### **Validaciones de Entrada:**
- **Longitud:** 10-2000 caracteres
- **Categorías:** Solo valores permitidos
- **Estados:** Solo valores permitidos
- **Prioridades:** Solo valores permitidos

### **Seguridad:**
- **SQL Injection:** Prevenido con parámetros preparados
- **XSS:** Sanitización de entrada
- **Autorización:** Verificación de permisos de admin
- **Rate Limiting:** Límites por usuario

### **Logging:**
- Todas las operaciones se registran
- Errores se capturan y reportan
- Auditoría completa de cambios

## 🧪 **Pruebas**

### **Script de Prueba:**
```bash
python test_suggestions_system.py
```

### **Pruebas Incluidas:**
1. ✅ Crear sugerencias de prueba
2. ✅ Listar sugerencias
3. ✅ Obtener estadísticas
4. ✅ Aprobar sugerencias
5. ✅ Rechazar sugerencias
6. ✅ Verificar estado final

## 📈 **Mantenimiento**

### **Limpieza Automática:**
```bash
# Limpiar sugerencias de más de 1 año
curl -X POST "http://localhost:9002/sugerencias/cleanup?days_to_keep=365"
```

### **Backup de Base de Datos:**
```bash
# Backup manual
cp suggestions.db suggestions_backup_$(date +%Y%m%d).db

# Restaurar backup
cp suggestions_backup_20241201.db suggestions.db
```

### **Monitoreo:**
- Verificar tamaño de la base de datos
- Monitorear número de sugerencias pendientes
- Revisar logs de errores
- Verificar rendimiento de consultas

## 🚀 **Despliegue**

### **Variables de Entorno:**
```bash
# Backend
BACKEND_URL=http://localhost:9002

# Bot de Telegram
TELEGRAM_TOKEN=your_bot_token
AUTHORIZED_TELEGRAM_USERS=user1,user2,user3
ADMIN_TELEGRAM_USERS=admin1,admin2
```

### **Archivos de Base de Datos:**
- `suggestions.db` - Base de datos principal
- `suggestions.db-journal` - Archivo de transacciones (temporal)

### **Logs:**
- `logs/backend_secure.log` - Logs del backend
- `logs/telegram_bot_secure.log` - Logs del bot

## 📝 **Ejemplos de Uso**

### **Ejemplo 1: Usuario Envía Sugerencia**
```
Usuario: /sugerencias
Bot: [Muestra menú de opciones]
Usuario: [Selecciona "Enviar Sugerencia"]
Bot: "Por favor, escribe tu sugerencia..."
Usuario: "Me gustaría que agreguen alertas por email"
Bot: "✅ ¡Sugerencia enviada exitosamente! ID: 123"
```

### **Ejemplo 2: Admin Gestiona Sugerencias**
```
Admin: /admin
Bot: [Muestra panel de administración]
Admin: [Selecciona "Gestionar Sugerencias"]
Bot: [Muestra sugerencias pendientes]
Admin: [Aproba sugerencia ID 123]
Bot: "✅ Sugerencia 123 aprobada exitosamente"
```

## 🔧 **Troubleshooting**

### **Problemas Comunes:**

1. **Error de conexión a la base de datos:**
   - Verificar permisos de archivo
   - Comprobar espacio en disco
   - Revisar logs de SQLite

2. **Sugerencias no se guardan:**
   - Verificar validación de entrada
   - Comprobar logs de error
   - Verificar conectividad del backend

3. **Bot no responde a comandos:**
   - Verificar token de Telegram
   - Comprobar logs del bot
   - Verificar handlers registrados

### **Comandos de Diagnóstico:**
```bash
# Verificar estado de la base de datos
sqlite3 suggestions.db ".tables"

# Ver sugerencias recientes
sqlite3 suggestions.db "SELECT * FROM suggestions ORDER BY created_at DESC LIMIT 5;"

# Ver estadísticas
sqlite3 suggestions.db "SELECT status, COUNT(*) FROM suggestions GROUP BY status;"
```

## 📚 **Referencias**

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Pydantic Models](https://pydantic-docs.helpmanual.io/)

---

**🎉 ¡El sistema de sugerencias está listo para usar!** 