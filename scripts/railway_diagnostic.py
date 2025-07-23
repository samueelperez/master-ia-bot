#!/usr/bin/env python3
"""
Script de diagnóstico específico para Railway
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path

def check_railway_config():
    """Verifica la configuración específica de Railway."""
    print("🔍 Verificando configuración de Railway...")
    print("=" * 50)
    
    # Verificar railway.toml
    if os.path.exists("railway.toml"):
        print("✅ railway.toml encontrado")
        try:
            with open("railway.toml", "r") as f:
                content = f.read()
                
            if "healthcheckPath = \"/\"" in content:
                print("✅ healthcheckPath configurado como '/'")
            else:
                print("❌ healthcheckPath no configurado como '/'")
                
            if "port = 8000" in content:
                print("✅ Puerto 8000 configurado")
            else:
                print("❌ Puerto 8000 no configurado")
                
        except Exception as e:
            print(f"❌ Error leyendo railway.toml: {e}")
    else:
        print("❌ railway.toml no encontrado")
    
    print()

def check_endpoints_order():
    """Verifica el orden de los endpoints en main_secure.py."""
    print("🔍 Verificando orden de endpoints en main_secure.py...")
    
    if os.path.exists("src/backend/main_secure.py"):
        try:
            with open("src/backend/main_secure.py", "r") as f:
                content = f.read()
                
            # Buscar el orden de los endpoints
            lines = content.split('\n')
            endpoint_order = []
            
            for i, line in enumerate(lines):
                if '@app.get(' in line:
                    endpoint = line.strip()
                    endpoint_order.append((i+1, endpoint))
            
            print("📋 Orden de endpoints encontrados:")
            for line_num, endpoint in endpoint_order[:10]:  # Mostrar solo los primeros 10
                print(f"   Línea {line_num}: {endpoint}")
            
            # Verificar que el endpoint raíz esté primero
            if endpoint_order and '"/"' in endpoint_order[0][1]:
                print("✅ Endpoint raíz '/' está definido primero")
            else:
                print("❌ Endpoint raíz '/' no está definido primero")
                
        except Exception as e:
            print(f"❌ Error leyendo main_secure.py: {e}")
    else:
        print("❌ main_secure.py no encontrado")
    
    print()

def check_middleware_order():
    """Verifica el orden de los middleware."""
    print("🔍 Verificando orden de middleware...")
    
    if os.path.exists("src/backend/main_secure.py"):
        try:
            with open("src/backend/main_secure.py", "r") as f:
                content = f.read()
                
            # Buscar middleware
            if "@app.middleware" in content:
                print("✅ Middleware de logging encontrado")
            else:
                print("❌ Middleware de logging no encontrado")
                
            if "TrustedHostMiddleware" in content:
                print("✅ TrustedHostMiddleware encontrado")
            else:
                print("❌ TrustedHostMiddleware no encontrado")
                
            if "CORSMiddleware" in content:
                print("✅ CORSMiddleware encontrado")
            else:
                print("❌ CORSMiddleware no encontrado")
                
            if "SecurityMiddleware" in content:
                print("✅ SecurityMiddleware encontrado")
            else:
                print("❌ SecurityMiddleware no encontrado")
                
        except Exception as e:
            print(f"❌ Error verificando middleware: {e}")
    else:
        print("❌ main_secure.py no encontrado")
    
    print()

def check_startup_sequence():
    """Verifica la secuencia de inicio."""
    print("🔍 Verificando secuencia de inicio...")
    
    if os.path.exists("start.sh"):
        try:
            with open("start.sh", "r") as f:
                content = f.read()
                
            if "uvicorn main_secure:app" in content:
                print("✅ Uvicorn configurado correctamente")
            else:
                print("❌ Uvicorn no configurado correctamente")
                
            if "--host 0.0.0.0" in content:
                print("✅ Host 0.0.0.0 configurado")
            else:
                print("❌ Host 0.0.0.0 no configurado")
                
            if "--port 8000" in content:
                print("✅ Puerto 8000 configurado")
            else:
                print("❌ Puerto 8000 no configurado")
                
        except Exception as e:
            print(f"❌ Error verificando start.sh: {e}")
    else:
        print("❌ start.sh no encontrado")
    
    print()

def check_dockerfile():
    """Verifica la configuración del Dockerfile."""
    print("🔍 Verificando Dockerfile...")
    
    if os.path.exists("Dockerfile"):
        try:
            with open("Dockerfile", "r") as f:
                content = f.read()
                
            if "EXPOSE" in content and "8000" in content:
                print("✅ Puerto 8000 expuesto en Dockerfile")
            else:
                print("❌ Puerto 8000 no expuesto en Dockerfile")
                
            if "CMD [\"/app/start.sh\"]" in content:
                print("✅ Comando de inicio configurado")
            else:
                print("❌ Comando de inicio no configurado")
                
            if "HEALTHCHECK" in content and "curl -f http://localhost:8000/" in content:
                print("✅ Healthcheck configurado para endpoint raíz")
            else:
                print("❌ Healthcheck no configurado para endpoint raíz")
                
        except Exception as e:
            print(f"❌ Error verificando Dockerfile: {e}")
    else:
        print("❌ Dockerfile no encontrado")
    
    print()

def generate_railway_recommendations():
    """Genera recomendaciones específicas para Railway."""
    print("💡 Recomendaciones para Railway...")
    print("=" * 50)
    
    recommendations = [
        "1. Verificar que el endpoint raíz '/' esté definido ANTES de cualquier middleware",
        "2. Asegurar que uvicorn esté configurado con --host 0.0.0.0 --port 8000",
        "3. Verificar que el healthcheckPath en railway.toml sea '/'",
        "4. Confirmar que el Dockerfile exponga el puerto 8000",
        "5. Verificar que no haya dependencias externas en el endpoint de healthcheck",
        "6. Asegurar que el servicio esté completamente inicializado antes del healthcheck",
        "7. Considerar aumentar el start-period en el healthcheck",
        "8. Verificar logs de Railway para errores específicos"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")
    
    print()

def main():
    """Función principal."""
    print("🚂 Diagnóstico Específico para Railway")
    print("=" * 50)
    
    check_railway_config()
    check_endpoints_order()
    check_middleware_order()
    check_startup_sequence()
    check_dockerfile()
    generate_railway_recommendations()
    
    print("🎯 Diagnóstico completado")
    print("📋 Revisa las recomendaciones arriba para solucionar el problema")

if __name__ == "__main__":
    main() 