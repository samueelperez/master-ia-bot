#!/usr/bin/env python3
"""
Script para configurar variables de entorno en Render
"""

import os
import sys
from datetime import datetime

def load_env_variables():
    """Carga las variables de entorno del archivo .env."""
    print("🔍 Cargando variables de entorno...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Variables de entorno cargadas")
        return True
    except ImportError:
        print("❌ python-dotenv no está instalado")
        return False

def get_supabase_variables():
    """Obtiene las variables de Supabase necesarias."""
    print("\n🔍 Variables de Supabase necesarias:")
    
    variables = {
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_ANON_KEY': os.getenv('SUPABASE_ANON_KEY'),
        'SUPABASE_SERVICE_ROLE_KEY': os.getenv('SUPABASE_SERVICE_ROLE_KEY'),
        'ADMIN_PASSWORD': os.getenv('ADMIN_PASSWORD'),
    }
    
    for key, value in variables.items():
        if value:
            print(f"✅ {key}: {value[:20]}..." if len(str(value)) > 20 else f"✅ {key}: {value}")
        else:
            print(f"❌ {key}: No configurada")
    
    return variables

def generate_render_commands(variables):
    """Genera los comandos para configurar Render."""
    print("\n🚀 COMANDOS PARA CONFIGURAR RENDER")
    print("=" * 60)
    print("Ejecuta estos comandos en tu terminal:")
    print()
    
    service_id = "srv-d20nmeemcj7s73dv0r7g"
    
    for key, value in variables.items():
        if value:
            # Escapar comillas y caracteres especiales
            escaped_value = str(value).replace('"', '\\"').replace("'", "\\'")
            print(f'render env set {service_id} {key} "{escaped_value}"')
    
    print()
    print("O usa la interfaz web:")
    print(f"🌐 https://dashboard.render.com/web/{service_id}/environment")
    print()

def show_manual_instructions():
    """Muestra instrucciones manuales."""
    print("📋 INSTRUCCIONES MANUALES")
    print("=" * 60)
    print("1. Ve a: https://dashboard.render.com/web/srv-d20nmeemcj7s73dv0r7g/environment")
    print("2. Haz clic en 'Add Environment Variable'")
    print("3. Agrega estas variables:")
    print()
    
    variables = [
        ('SUPABASE_URL', 'https://baotpqenzaicldzgeinu.supabase.co'),
        ('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJhb3RwcWVuemFpY2xkemdlaW51Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM2NDA3MjAsImV4cCI6MjA2OTIxNjcyMH0.bZbFYJgGOdPzVvTDQoo-CTDc0r8PMCfAunv3s3TlcZ4'),
        ('SUPABASE_SERVICE_ROLE_KEY', 'OBTENER DESDE SUPABASE DASHBOARD'),
        ('ADMIN_PASSWORD', 'masteradmin123'),
    ]
    
    for key, value in variables:
        print(f"   {key}: {value}")
    
    print()
    print("4. Haz clic en 'Save Changes'")
    print("5. El servicio se reiniciará automáticamente")

def check_supabase_service_role():
    """Verifica si necesitamos la service role key."""
    print("\n🔍 IMPORTANTE: Service Role Key")
    print("=" * 60)
    print("Para obtener la SUPABASE_SERVICE_ROLE_KEY:")
    print("1. Ve a: https://supabase.com/dashboard/project/baotpqenzaicldzgeinu/settings/api")
    print("2. Copia la 'service_role' key (no la anon key)")
    print("3. Esta key tiene permisos completos para bypass RLS")
    print()

def main():
    """Función principal."""
    print("🚀 CONFIGURACIÓN DE VARIABLES EN RENDER")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Cargar variables de entorno
    if not load_env_variables():
        return False
    
    # Obtener variables de Supabase
    variables = get_supabase_variables()
    
    # Verificar service role key
    check_supabase_service_role()
    
    # Generar comandos
    generate_render_commands(variables)
    
    # Mostrar instrucciones manuales
    show_manual_instructions()
    
    print("\n" + "=" * 60)
    print("✅ CONFIGURACIÓN COMPLETA")
    print("=" * 60)
    print("Después de configurar las variables:")
    print("1. El servicio se reiniciará automáticamente")
    print("2. Prueba el bot de Telegram")
    print("3. Los comandos /sugerencias y /admin deberían funcionar")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 