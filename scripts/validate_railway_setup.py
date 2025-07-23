#!/usr/bin/env python3
"""
Script de validación para configuración de Railway
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_file_exists(file_path, description):
    """Verifica que un archivo existe."""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NO ENCONTRADO")
        return False

def check_railway_config():
    """Verifica la configuración de Railway."""
    print("🔍 Verificando configuración de Railway...")
    print("=" * 50)
    
    # Verificar archivos de configuración
    files_to_check = [
        ("railway.toml", "Configuración de Railway"),
        ("railway.json", "Configuración JSON de Railway"),
        ("start.sh", "Script de inicio"),
        ("Dockerfile", "Dockerfile"),
        ("src/backend/main_secure.py", "Backend principal"),
        ("requirements/common.txt", "Dependencias Python")
    ]
    
    all_files_exist = True
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_files_exist = False
    
    print()
    
    # Verificar configuración de railway.toml
    if os.path.exists("railway.toml"):
        print("📋 Verificando railway.toml...")
        try:
            with open("railway.toml", "r") as f:
                content = f.read()
                
            if "healthcheckPath" in content:
                print("✅ healthcheckPath configurado")
            else:
                print("❌ healthcheckPath no encontrado")
                all_files_exist = False
                
            if "port = 8000" in content:
                print("✅ Puerto 8000 configurado")
            else:
                print("❌ Puerto 8000 no configurado")
                all_files_exist = False
                
        except Exception as e:
            print(f"❌ Error leyendo railway.toml: {e}")
            all_files_exist = False
    
    print()
    
    # Verificar endpoints en main_secure.py
    if os.path.exists("src/backend/main_secure.py"):
        print("🔍 Verificando endpoints en main_secure.py...")
        try:
            with open("src/backend/main_secure.py", "r") as f:
                content = f.read()
                
            endpoints = [
                ("/railway-health", "Endpoint Railway Health"),
                ("/healthcheck-railway", "Endpoint Healthcheck Railway"),
                ("/health", "Endpoint Health"),
                ("/test", "Endpoint Test")
            ]
            
            for endpoint, description in endpoints:
                if f'@app.get("{endpoint}")' in content:
                    print(f"✅ {description}: {endpoint}")
                else:
                    print(f"❌ {description}: {endpoint} - NO ENCONTRADO")
                    all_files_exist = False
                    
        except Exception as e:
            print(f"❌ Error leyendo main_secure.py: {e}")
            all_files_exist = False
    
    print()
    
    # Verificar script de inicio
    if os.path.exists("start.sh"):
        print("🔍 Verificando start.sh...")
        try:
            with open("start.sh", "r") as f:
                content = f.read()
                
            if "uvicorn main_secure:app" in content:
                print("✅ Uvicorn configurado correctamente")
            else:
                print("❌ Uvicorn no configurado correctamente")
                all_files_exist = False
                
            if "--port 8000" in content:
                print("✅ Puerto 8000 configurado en start.sh")
            else:
                print("❌ Puerto 8000 no configurado en start.sh")
                all_files_exist = False
                
        except Exception as e:
            print(f"❌ Error leyendo start.sh: {e}")
            all_files_exist = False
    
    print()
    
    # Verificar Dockerfile
    if os.path.exists("Dockerfile"):
        print("🔍 Verificando Dockerfile...")
        try:
            with open("Dockerfile", "r") as f:
                content = f.read()
                
            if "EXPOSE" in content and "8000" in content:
                print("✅ Puerto 8000 expuesto en Dockerfile")
            else:
                print("❌ Puerto 8000 no expuesto en Dockerfile")
                all_files_exist = False
                
            if "CMD [\"/app/start.sh\"]" in content:
                print("✅ Comando de inicio configurado")
            else:
                print("❌ Comando de inicio no configurado")
                all_files_exist = False
                
        except Exception as e:
            print(f"❌ Error leyendo Dockerfile: {e}")
            all_files_exist = False
    
    print()
    print("=" * 50)
    
    if all_files_exist:
        print("🎉 Configuración de Railway válida")
        return True
    else:
        print("❌ Configuración de Railway tiene problemas")
        return False

def main():
    """Función principal."""
    print("🚂 Validación de Configuración Railway")
    print("=" * 50)
    
    success = check_railway_config()
    
    if success:
        print("\n✅ Validación completada exitosamente")
        print("🚀 El proyecto está listo para Railway")
        sys.exit(0)
    else:
        print("\n❌ Validación falló")
        print("🔧 Revisa los problemas identificados arriba")
        sys.exit(1)

if __name__ == "__main__":
    main() 