#!/usr/bin/env python3
"""
Script para verificar las tablas de Supabase
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar variables de entorno manualmente si no están en .env
if not os.getenv('SUPABASE_URL'):
    os.environ['SUPABASE_URL'] = 'https://baotpqenzaicldzgeinu.supabase.co'
if not os.getenv('SUPABASE_ANON_KEY'):
    os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJhb3RwcWVuemFpY2xkemdlaW51Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM2NDA3MjAsImV4cCI6MjA2OTIxNjcyMH0.bZbFYJgGOdPzVvTDQoo-CTDc0r8PMCfAunv3s3TlcZ4'

def check_tables():
    """Verifica que las tablas existan en Supabase."""
    print("🔍 Verificando tablas en Supabase...")
    
    try:
        from supabase import create_client
        
        # Crear cliente
        supabase = create_client(
            os.environ['SUPABASE_URL'],
            os.environ['SUPABASE_ANON_KEY']
        )
        
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
        existing_tables = []
        
        for table in required_tables:
            try:
                # Intentar hacer una consulta simple
                result = supabase.table(table).select('id').limit(1).execute()
                print(f"✅ Tabla {table}: Existe")
                existing_tables.append(table)
            except Exception as e:
                print(f"❌ Tabla {table}: No existe o error - {e}")
                missing_tables.append(table)
        
        print(f"\n📊 Resumen:")
        print(f"✅ Tablas existentes: {len(existing_tables)}")
        print(f"❌ Tablas faltantes: {len(missing_tables)}")
        
        if missing_tables:
            print(f"\n⚠️  Tablas que necesitan ser creadas:")
            for table in missing_tables:
                print(f"   - {table}")
            print(f"\n💡 Ejecuta el script SQL en Supabase para crear las tablas faltantes.")
            return False
        else:
            print(f"\n🎉 ¡Todas las tablas están creadas correctamente!")
            return True
            
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return False

def test_suggestion_creation():
    """Prueba la creación de una sugerencia."""
    print("\n🔍 Probando creación de sugerencia...")
    
    try:
        from supabase import create_client
        
        supabase = create_client(
            os.environ['SUPABASE_URL'],
            os.environ['SUPABASE_ANON_KEY']
        )
        
        # Crear una sugerencia de prueba
        test_suggestion = {
            'user_id': 999999,  # ID de prueba
            'suggestion_text': f'Prueba de configuración - {os.urandom(8).hex()}',
            'user_info': {'test': True},
            'status': 'pending'
        }
        
        result = supabase.table('suggestions').insert(test_suggestion).execute()
        
        if result.data:
            print("✅ Sugerencia creada exitosamente")
            
            # Obtener sugerencias
            suggestions = supabase.table('suggestions').select('*').limit(5).execute()
            if suggestions.data:
                print(f"✅ Lectura de sugerencias exitosa ({len(suggestions.data)} sugerencias)")
            
            return True
        else:
            print("❌ Error creando sugerencia")
            return False
            
    except Exception as e:
        print(f"❌ Error probando sugerencias: {e}")
        return False

def test_user_creation():
    """Prueba la creación de un usuario."""
    print("\n🔍 Probando creación de usuario...")
    
    try:
        from supabase import create_client
        
        supabase = create_client(
            os.environ['SUPABASE_URL'],
            os.environ['SUPABASE_ANON_KEY']
        )
        
        # Crear un usuario de prueba
        test_user = {
            'telegram_id': 888888,
            'username': 'test_user',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True
        }
        
        result = supabase.table('telegram_users').upsert(test_user, on_conflict='telegram_id').execute()
        
        if result.data:
            print("✅ Usuario creado/actualizado exitosamente")
            
            # Obtener usuario
            user = supabase.table('telegram_users').select('*').eq('telegram_id', 888888).execute()
            if user.data:
                print("✅ Usuario recuperado exitosamente")
            
            return True
        else:
            print("❌ Error creando/actualizando usuario")
            return False
            
    except Exception as e:
        print(f"❌ Error probando usuarios: {e}")
        return False

def main():
    """Función principal."""
    print("🚀 VERIFICACIÓN DE TABLAS DE SUPABASE")
    print("=" * 50)
    
    # Verificar tablas
    tables_ok = check_tables()
    
    if tables_ok:
        # Probar funcionalidades
        suggestion_ok = test_suggestion_creation()
        user_ok = test_user_creation()
        
        print(f"\n📊 RESULTADOS:")
        print(f"✅ Tablas: {'OK' if tables_ok else 'ERROR'}")
        print(f"✅ Sugerencias: {'OK' if suggestion_ok else 'ERROR'}")
        print(f"✅ Usuarios: {'OK' if user_ok else 'ERROR'}")
        
        if tables_ok and suggestion_ok and user_ok:
            print(f"\n🎉 ¡Todo está funcionando perfectamente!")
            return True
        else:
            print(f"\n⚠️  Algunas funcionalidades tienen problemas.")
            return False
    else:
        print(f"\n❌ Las tablas no están creadas. Ejecuta el script SQL en Supabase.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 