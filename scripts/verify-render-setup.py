#!/usr/bin/env python3
"""
Script de verificación para configuración de Render.com
Valida que todos los componentes necesarios estén listos para el despliegue.
"""

import os
import sys
import importlib
from pathlib import Path

def check_python_version():
    """Verificar versión de Python."""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 11:
        print("✅ Versión de Python compatible")
        return True
    else:
        print("❌ Se requiere Python 3.11+")
        return False

def check_dependencies():
    """Verificar dependencias críticas."""
    critical_deps = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'psycopg2',
        'pydantic',
        'requests'
    ]
    
    print("\n📦 Verificando dependencias críticas...")
    missing_deps = []
    
    for dep in critical_deps:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - FALTANTE")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"\n⚠️ Dependencias faltantes: {', '.join(missing_deps)}")
        print("Ejecuta: pip install -r requirements/common.txt")
        return False
    
    return True

def check_files():
    """Verificar archivos críticos."""
    critical_files = [
        'src/backend/main_secure.py',
        'src/backend/core/db.py',
        'src/backend/core/config/security_config.py',
        'requirements/common.txt',
        'render.yaml'
    ]
    
    print("\n📁 Verificando archivos críticos...")
    missing_files = []
    
    for file_path in critical_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NO ENCONTRADO")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    return True

def check_environment_vars():
    """Verificar variables de entorno críticas."""
    critical_vars = [
        'DATABASE_URL',
        'BACKEND_API_SECRET_KEY',
        'ENVIRONMENT'
    ]
    
    print("\n🔧 Verificando variables de entorno...")
    missing_vars = []
    
    for var in critical_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} = {'*' * len(value)}")
        else:
            print(f"❌ {var} - NO CONFIGURADA")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️ Variables faltantes: {', '.join(missing_vars)}")
        print("Configura estas variables en Render Dashboard")
        return False
    
    return True

def check_backend_endpoints():
    """Verificar que el backend tenga endpoints críticos."""
    backend_file = Path('src/backend/main_secure.py')
    
    if not backend_file.exists():
        print("❌ No se puede verificar endpoints - main_secure.py no encontrado")
        return False
    
    print("\n🔗 Verificando endpoints críticos...")
    
    with open(backend_file, 'r') as f:
        content = f.read()
    
    critical_endpoints = [
        ('/ping', 'GET'),
        ('/health', 'GET'),
        ('/healthcheck', 'GET')
    ]
    
    missing_endpoints = []
    
    for endpoint, method in critical_endpoints:
        if f'@app.{method.lower()}("{endpoint}")' in content:
            print(f"✅ {method} {endpoint}")
        else:
            print(f"❌ {method} {endpoint} - NO ENCONTRADO")
            missing_endpoints.append(f"{method} {endpoint}")
    
    if missing_endpoints:
        print(f"\n⚠️ Endpoints faltantes: {', '.join(missing_endpoints)}")
        return False
    
    return True

def main():
    """Función principal de verificación."""
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN PARA RENDER")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_files(),
        check_environment_vars(),
        check_backend_endpoints()
    ]
    
    print("\n" + "=" * 50)
    
    if all(checks):
        print("🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        print("✅ Tu proyecto está listo para desplegar en Render")
        print("\n📋 Próximos pasos:")
        print("1. Ve a render.com y crea una cuenta")
        print("2. Conecta tu repositorio de GitHub")
        print("3. Crea un nuevo Web Service")
        print("4. Configura las variables de entorno en Render Dashboard")
        print("5. ¡Deploy automático!")
        return True
    else:
        print("❌ ALGUNAS VERIFICACIONES FALLARON")
        print("⚠️ Corrige los problemas antes de desplegar")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 