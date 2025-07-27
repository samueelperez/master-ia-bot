#!/usr/bin/env python3
"""
Script de verificación de configuración de Supabase
Verifica que todas las tablas y configuraciones estén correctas
"""

import os
import sys
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cargar variables de entorno
load_dotenv()

def check_environment_variables():
    """Verifica que las variables de entorno estén configuradas."""
    print("🔍 Verificando variables de entorno...")
    
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY',
        'ADMIN_PASSWORD'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {'*' * len(value)}")
    
    if missing_vars:
        print(f"❌ Variables faltantes: {', '.join(missing_vars)}")
        return False
    
    print("✅ Todas las variables de entorno están configuradas")
    return True

def test_supabase_connection():
    """Prueba la conexión con Supabase."""
    print("\n🔍 Probando conexión con Supabase...")
    
    try:
        from src.backend.core.supabase_config import supabase_service
        
        if not supabase_service.config.enabled:
            print("❌ Supabase no está habilitado")
            return False
        
        # Probar conexión
        if supabase_service.config.test_connection():
            print("✅ Conexión a Supabase exitosa")
            return True
        else:
            print("❌ Error conectando a Supabase")
            return False
            
    except Exception as e:
        print(f"❌ Error probando Supabase: {e}")
        return False

def test_telegram_bot_supabase():
    """Prueba la configuración de Supabase en el bot de Telegram."""
    print("\n🔍 Probando configuración de Supabase en Telegram Bot...")
    
    try:
        from src.telegram_bot.core.supabase_config import supabase_service
        
        if not supabase_service.config.enabled:
            print("❌ Supabase no está habilitado en Telegram Bot")
            return False
        
        print("✅ Supabase configurado correctamente en Telegram Bot")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración de Telegram Bot: {e}")
        return False

def test_database_tables():
    """Prueba que las tablas existan en Supabase."""
    print("\n🔍 Verificando tablas en Supabase...")
    
    try:
        from src.backend.core.supabase_config import supabase_service
        
        if not supabase_service.config.enabled:
            print("❌ Supabase no está habilitado")
            return False
        
        # Lista de tablas que deben existir
        required_tables = [
            'telegram_users',
            'suggestions',
            'alerts',
            'user_configurations',
            'activity_logs',
            'technical_analyses',
            'trading_signals'
        ]
        
        missing_tables = []
        for table in required_tables:
            try:
                # Intentar hacer una consulta simple
                result = supabase_service.client.table(table).select('id').limit(1).execute()
                print(f"✅ Tabla {table}: Existe")
            except Exception as e:
                print(f"❌ Tabla {table}: No existe o error - {e}")
                missing_tables.append(table)
        
        if missing_tables:
            print(f"❌ Tablas faltantes: {', '.join(missing_tables)}")
            return False
        
        print("✅ Todas las tablas existen")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return False

def test_suggestion_creation():
    """Prueba la creación de una sugerencia."""
    print("\n🔍 Probando creación de sugerencia...")
    
    try:
        from src.telegram_bot.core.supabase_config import supabase_service
        
        if not supabase_service.config.enabled:
            print("❌ Supabase no está habilitado")
            return False
        
        # Crear una sugerencia de prueba
        test_suggestion = f"Prueba de configuración - {datetime.now().isoformat()}"
        result = supabase_service.create_suggestion(
            user_id=999999,  # ID de prueba
            suggestion_text=test_suggestion,
            user_info={"test": True}
        )
        
        if result.get("status") == "success":
            print("✅ Sugerencia creada exitosamente")
            
            # Limpiar la sugerencia de prueba
            suggestions = supabase_service.get_suggestions(limit=1)
            if suggestions:
                print("✅ Lectura de sugerencias exitosa")
            
            return True
        else:
            print(f"❌ Error creando sugerencia: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando sugerencias: {e}")
        return False

def test_user_management():
    """Prueba la gestión de usuarios."""
    print("\n🔍 Probando gestión de usuarios...")
    
    try:
        from src.telegram_bot.core.supabase_config import supabase_service
        
        if not supabase_service.config.enabled:
            print("❌ Supabase no está habilitado")
            return False
        
        # Crear/actualizar usuario de prueba
        test_user_id = 888888
        success = supabase_service.create_or_update_user(
            telegram_id=test_user_id,
            username="test_user",
            first_name="Test",
            last_name="User"
        )
        
        if success:
            print("✅ Usuario creado/actualizado exitosamente")
            
            # Obtener usuario
            user = supabase_service.get_user(test_user_id)
            if user:
                print("✅ Usuario recuperado exitosamente")
                return True
            else:
                print("❌ No se pudo recuperar el usuario")
                return False
        else:
            print("❌ Error creando/actualizando usuario")
            return False
            
    except Exception as e:
        print(f"❌ Error probando gestión de usuarios: {e}")
        return False

def main():
    """Función principal de verificación."""
    print("🚀 VERIFICACIÓN DE CONFIGURACIÓN DE SUPABASE")
    print("=" * 50)
    
    checks = [
        ("Variables de entorno", check_environment_variables),
        ("Conexión Supabase", test_supabase_connection),
        ("Telegram Bot Supabase", test_telegram_bot_supabase),
        ("Tablas de base de datos", test_database_tables),
        ("Creación de sugerencias", test_suggestion_creation),
        ("Gestión de usuarios", test_user_management)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error en {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las verificaciones pasaron! Supabase está configurado correctamente.")
        return True
    else:
        print("⚠️  Algunas verificaciones fallaron. Revisa la configuración.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 