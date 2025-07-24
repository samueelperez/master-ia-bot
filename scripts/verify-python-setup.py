#!/usr/bin/env python3
"""
Script de verificación para Python directo en Render
"""

import sys
import os
import importlib

def check_python_version():
    """Verificar versión de Python"""
    print(f"🐍 Python version: {sys.version}")
    if sys.version_info >= (3, 11):
        print("✅ Python 3.11+ OK")
        return True
    else:
        print("❌ Python 3.11+ requerido")
        return False

def check_dependencies():
    """Verificar dependencias críticas"""
    critical_deps = [
        "fastapi",
        "uvicorn", 
        "requests",
        "psutil",
        "sqlalchemy"
    ]
    
    missing_deps = []
    for dep in critical_deps:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep} - OK")
        except ImportError:
            print(f"❌ {dep} - FALTANTE")
            missing_deps.append(dep)
    
    return len(missing_deps) == 0

def check_files():
    """Verificar archivos críticos"""
    critical_files = [
        "src/backend/main_secure.py",
        "requirements/common.txt",
        "render.yaml"
    ]
    
    missing_files = []
    for file_path in critical_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - EXISTE")
        else:
            print(f"❌ {file_path} - NO EXISTE")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def check_environment():
    """Verificar variables de entorno"""
    env_vars = [
        "PYTHON_VERSION",
        "BACKEND_PORT", 
        "ENVIRONMENT"
    ]
    
    missing_vars = []
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}={value}")
        else:
            print(f"❌ {var} - NO CONFIGURADA")
            missing_vars.append(var)
    
    return len(missing_vars) == 0

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN PYTHON DIRECTO")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Files", check_files),
        ("Environment", check_environment)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        if not check_func():
            all_passed = False
    
    print(f"\n{'=' * 50}")
    if all_passed:
        print("🎉 TODAS LAS VERIFICACIONES PASARON")
        print("✅ Configuración lista para Render")
        return 0
    else:
        print("❌ ALGUNAS VERIFICACIONES FALLARON")
        print("🔧 Revisar configuración antes de deploy")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 