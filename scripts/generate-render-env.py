#!/usr/bin/env python3
"""
Script para generar variables de entorno para Render.com
Genera valores seguros para todas las variables necesarias.
"""

import secrets
import string
import os
from datetime import datetime

def generate_secret_key(length=64):
    """Generar una clave secreta segura."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_api_key(length=32):
    """Generar una API key segura."""
    return secrets.token_urlsafe(length)

def main():
    """Generar todas las variables de entorno necesarias."""
    print("🔧 GENERADOR DE VARIABLES DE ENTORNO PARA RENDER")
    print("=" * 60)
    print()
    
    # Variables críticas con valores generados
    env_vars = {
        # Configuración básica
        "PYTHON_VERSION": "3.11",
        "BACKEND_PORT": "8000",
        "ENVIRONMENT": "production",
        "ENABLE_DOCS": "false",
        
        # Seguridad (generadas automáticamente)
        "BACKEND_API_SECRET_KEY": generate_api_key(32),
        "SECRET_KEY": generate_secret_key(64),
        "JWT_SECRET_KEY": generate_secret_key(64),
        "ENCRYPTION_KEY": generate_secret_key(32),
        
        # CORS y Hosts (actualizar con tu dominio real)
        "BACKEND_ALLOWED_ORIGINS": "https://tu-app.onrender.com,http://localhost:3000",
        "BACKEND_ALLOWED_HOSTS": "tu-app.onrender.com,localhost,127.0.0.1",
        
        # Rate Limiting
        "BACKEND_RATE_LIMIT_PER_MINUTE": "60",
        "BACKEND_RATE_LIMIT_PER_HOUR": "1000",
        "BACKEND_RATE_LIMIT_PER_DAY": "10000",
        
        # Timeouts
        "BACKEND_HTTP_TIMEOUT": "30",
        "BACKEND_DB_TIMEOUT": "10",
        "BACKEND_CCXT_TIMEOUT": "15",
        
        # Límites de datos
        "BACKEND_MAX_LIMIT_OHLCV": "1000",
        "BACKEND_MAX_INDICATORS_PER_REQUEST": "50",
        "BACKEND_MAX_PAYLOAD_SIZE": "1048576",
        
        # Exchange configuración
        "BACKEND_DEFAULT_EXCHANGE": "binance",
        "BACKEND_EXCHANGE_SANDBOX": "true",
    }
    
    print("📋 VARIABLES CRÍTICAS (OBLIGATORIAS):")
    print("-" * 40)
    
    critical_vars = [
        "PYTHON_VERSION", "BACKEND_PORT", "ENVIRONMENT", "ENABLE_DOCS",
        "BACKEND_API_SECRET_KEY", "SECRET_KEY", "JWT_SECRET_KEY", "ENCRYPTION_KEY",
        "BACKEND_ALLOWED_ORIGINS", "BACKEND_ALLOWED_HOSTS"
    ]
    
    for var in critical_vars:
        value = env_vars[var]
        print(f"{var}={value}")
    
    print()
    print("📋 VARIABLES DE BASE DE DATOS:")
    print("-" * 40)
    print("# IMPORTANTE: Configura una de estas opciones:")
    print()
    print("# Opción 1: Supabase (Gratis)")
    print("DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres")
    print()
    print("# Opción 2: Neon (Gratis)")
    print("DATABASE_URL=postgresql://[user]:[password]@[host]/[database]?sslmode=require")
    print()
    print("# Opción 3: Railway (Gratis) - Alternativa (no recomendado)")
    print("DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[database]")
    
    print()
    print("📋 VARIABLES OPCIONALES (APIs Externas):")
    print("-" * 40)
    
    optional_vars = [
        "BINANCE_API_KEY", "BINANCE_SECRET_KEY", "BINANCE_TESTNET",
        "ALPHA_VANTAGE_API_KEY", "NEWS_API_KEY", "TWITTER_BEARER_TOKEN",
        "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "OPENAI_API_KEY"
    ]
    
    for var in optional_vars:
        print(f"{var}=tu_{var.lower()}_aqui")
    
    print()
    print("📋 VARIABLES DE RATE LIMITING:")
    print("-" * 40)
    
    rate_limit_vars = [
        "BACKEND_RATE_LIMIT_PER_MINUTE", "BACKEND_RATE_LIMIT_PER_HOUR", 
        "BACKEND_RATE_LIMIT_PER_DAY", "BACKEND_HTTP_TIMEOUT", 
        "BACKEND_DB_TIMEOUT", "BACKEND_CCXT_TIMEOUT"
    ]
    
    for var in rate_limit_vars:
        value = env_vars[var]
        print(f"{var}={value}")
    
    print()
    print("📋 VARIABLES DE LÍMITES DE DATOS:")
    print("-" * 40)
    
    limit_vars = [
        "BACKEND_MAX_LIMIT_OHLCV", "BACKEND_MAX_INDICATORS_PER_REQUEST",
        "BACKEND_MAX_PAYLOAD_SIZE", "BACKEND_DEFAULT_EXCHANGE", "BACKEND_EXCHANGE_SANDBOX"
    ]
    
    for var in limit_vars:
        value = env_vars[var]
        print(f"{var}={value}")
    
    print()
    print("🚨 INSTRUCCIONES IMPORTANTES:")
    print("=" * 60)
    print()
    print("1. 📝 COPIA estas variables al Dashboard de Render:")
    print("   - Ve a tu Web Service en Render")
    print("   - Click en 'Environment'")
    print("   - Agrega cada variable una por una")
    print()
    print("2. 🔄 ACTUALIZA las URLs con tu dominio real:")
    print("   - Reemplaza 'tu-app.onrender.com' con tu dominio real")
    print("   - Ejemplo: 'crypto-ai-bot-backend.onrender.com'")
    print()
    print("3. 🗄️ CONFIGURA la base de datos:")
    print("   - Crea una base de datos PostgreSQL (Supabase/Neon)")
    print("   - Copia la DATABASE_URL a Render")
    print()
    print("4. 🔑 GENERA nuevas claves secretas:")
    print("   - Las claves generadas son seguras")
    print("   - Puedes regenerarlas ejecutando este script nuevamente")
    print()
    print("5. ✅ VERIFICA la configuración:")
    print("   - Ejecuta: python scripts/verify-render-setup.py")
    print()
    
    # Generar archivo .env.example para Render
    env_file_content = "# Variables de entorno para Render.com\n"
    env_file_content += f"# Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for var, value in env_vars.items():
        env_file_content += f"{var}={value}\n"
    
    env_file_content += "\n# IMPORTANTE: Configura DATABASE_URL con tu base de datos real\n"
    env_file_content += "DATABASE_URL=postgresql://username:password@host:5432/database\n"
    
    # Guardar archivo
    with open("config/render.env.example", "w") as f:
        f.write(env_file_content)
    
    print("💾 ARCHIVO GENERADO:")
    print("   config/render.env.example")
    print("   (Puedes usar este archivo como referencia)")
    
    print()
    print("🎉 ¡VARIABLES GENERADAS EXITOSAMENTE!")
    print("   Ahora puedes configurarlas en Render Dashboard")

if __name__ == "__main__":
    main() 