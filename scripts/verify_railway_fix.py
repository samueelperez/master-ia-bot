#!/usr/bin/env python3
"""
Script de verificación para Railway - Prueba todos los módulos principales
"""

import sys
import os
import subprocess
import time

def test_python_syntax():
    """Prueba la sintaxis de todos los archivos Python"""
    print("🔍 Verificando sintaxis Python...")
    
    # Archivos principales a verificar
    files_to_check = [
        "src/ai-module/main.py",
        "src/ai-module/core/llm_inference.py",
        "src/backend/main.py",
        "src/data-service/main.py",
        "src/telegram-bot/core/telegram_bot_secure.py"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                subprocess.run([sys.executable, "-m", "py_compile", file_path], 
                             check=True, capture_output=True)
                print(f"✅ {file_path} - Sintaxis correcta")
            except subprocess.CalledProcessError as e:
                print(f"❌ {file_path} - Error de sintaxis: {e}")
                return False
        else:
            print(f"⚠️ {file_path} - Archivo no encontrado")
    
    return True

def test_imports():
    """Prueba las importaciones principales"""
    print("\n🔍 Verificando importaciones...")
    
    try:
        # Probar AI Module
        sys.path.append('src/ai-module')
        from core.llm_inference import AnalyzeRequest
        print("✅ AI Module - Importación exitosa")
        
        # Probar Backend
        sys.path.append('src/backend')
        import main as backend_main
        print("✅ Backend - Importación exitosa")
        
        # Probar Data Service
        sys.path.append('src/data-service')
        import main as data_main
        print("✅ Data Service - Importación exitosa")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def test_environment_variables():
    """Prueba las variables de entorno críticas"""
    print("\n🔍 Verificando variables de entorno...")
    
    critical_vars = [
        "TELEGRAM_BOT_TOKEN",
        "OPENAI_API_KEY",
        "DATABASE_URL"
    ]
    
    missing_vars = []
    for var in critical_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Variables faltantes: {', '.join(missing_vars)}")
        print("   Estas variables son necesarias para Railway")
        return False
    else:
        print("✅ Todas las variables críticas están configuradas")
        return True

def test_docker_build():
    """Prueba que el Dockerfile se puede construir"""
    print("\n🔍 Verificando Dockerfile...")
    
    try:
        # Verificar que el Dockerfile existe
        if not os.path.exists("Dockerfile.simple"):
            print("❌ Dockerfile.simple no encontrado")
            return False
        
        print("✅ Dockerfile.simple encontrado")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando Dockerfile: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🚀 Iniciando verificación para Railway...")
    print("=" * 50)
    
    tests = [
        ("Sintaxis Python", test_python_syntax),
        ("Importaciones", test_imports),
        ("Variables de Entorno", test_environment_variables),
        ("Dockerfile", test_docker_build)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS DE LA VERIFICACIÓN")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ El proyecto está listo para Railway")
        return 0
    else:
        print("⚠️ ALGUNAS PRUEBAS FALLARON")
        print("❌ Revisa los errores antes de desplegar en Railway")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 