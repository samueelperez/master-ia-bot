#!/usr/bin/env python3
"""
Script para analizar logs de Railway y detectar errores específicos
"""

import re
import sys
from datetime import datetime

def analyze_railway_logs(log_content):
    """Analiza logs de Railway para detectar errores específicos"""
    
    print("🔍 ANALIZANDO LOGS DE RAILWAY")
    print("=" * 50)
    
    # Patrones de error comunes
    error_patterns = {
        "import_error": r"ImportError|ModuleNotFoundError",
        "syntax_error": r"SyntaxError|IndentationError",
        "connection_error": r"ConnectionError|Connection refused",
        "port_error": r"Address already in use|Port.*already in use",
        "permission_error": r"Permission denied|PermissionError",
        "timeout_error": r"Timeout|timeout",
        "memory_error": r"MemoryError|Out of memory",
        "uvicorn_error": r"uvicorn.*error|Uvicorn.*failed",
        "python_error": r"Python.*error|python.*failed",
        "healthcheck_error": r"healthcheck.*failed|Health check.*failed"
    }
    
    # Contar líneas totales
    total_lines = len(log_content.split('\n'))
    print(f"📊 Total de líneas en logs: {total_lines}")
    
    # Buscar errores
    found_errors = {}
    
    for error_type, pattern in error_patterns.items():
        matches = re.findall(pattern, log_content, re.IGNORECASE)
        if matches:
            found_errors[error_type] = matches
            print(f"\n❌ {error_type.upper()}: {len(matches)} ocurrencias")
            for match in matches[:3]:  # Mostrar solo los primeros 3
                print(f"   - {match}")
    
    # Buscar patrones específicos de Railway
    railway_patterns = {
        "build_success": r"Build time:.*seconds",
        "healthcheck_fail": r"Attempt #\d+ failed with service unavailable",
        "service_start": r"Started server process|Uvicorn running on",
        "service_stop": r"Application shutdown|Shutting down",
        "port_listen": r"Listening on.*:8000",
        "curl_error": r"curl.*failed|curl.*error"
    }
    
    print(f"\n🔍 PATRONES ESPECÍFICOS DE RAILWAY:")
    for pattern_name, pattern in railway_patterns.items():
        matches = re.findall(pattern, log_content, re.IGNORECASE)
        if matches:
            print(f"✅ {pattern_name}: {len(matches)} ocurrencias")
            for match in matches[:2]:
                print(f"   - {match}")
        else:
            print(f"❌ {pattern_name}: No encontrado")
    
    # Buscar líneas con errores específicos
    print(f"\n🚨 LÍNEAS CON ERRORES CRÍTICOS:")
    error_lines = []
    for line in log_content.split('\n'):
        if any(keyword in line.lower() for keyword in ['error', 'failed', 'exception', 'traceback']):
            error_lines.append(line.strip())
    
    for line in error_lines[:10]:  # Mostrar solo los primeros 10 errores
        print(f"   {line}")
    
    # Análisis de timing
    print(f"\n⏱️ ANÁLISIS DE TIMING:")
    build_time_match = re.search(r"Build time: ([\d.]+) seconds", log_content)
    if build_time_match:
        build_time = float(build_time_match.group(1))
        print(f"   Build time: {build_time} segundos")
        if build_time > 300:
            print(f"   ⚠️ Build muy lento (>5 minutos)")
    
    # Buscar intentos de healthcheck
    healthcheck_attempts = re.findall(r"Attempt #(\d+)", log_content)
    if healthcheck_attempts:
        max_attempt = max(int(attempt) for attempt in healthcheck_attempts)
        print(f"   Healthcheck attempts: {max_attempt}")
        if max_attempt > 10:
            print(f"   ⚠️ Demasiados intentos de healthcheck")
    
    return found_errors

def suggest_solutions(errors_found):
    """Sugiere soluciones basadas en los errores encontrados"""
    
    print(f"\n💡 SUGERENCIAS DE SOLUCIÓN:")
    print("=" * 50)
    
    if not errors_found:
        print("✅ No se encontraron errores específicos")
        print("💡 El problema puede ser de configuración o timing")
        return
    
    solutions = {
        "import_error": [
            "Verificar que todas las dependencias estén instaladas",
            "Revisar requirements/common.txt",
            "Verificar imports en main_secure.py"
        ],
        "syntax_error": [
            "Verificar sintaxis de Python en main_secure.py",
            "Ejecutar: python -m py_compile main_secure.py",
            "Revisar indentación y caracteres especiales"
        ],
        "connection_error": [
            "Verificar que el puerto 8000 esté disponible",
            "Revisar configuración de uvicorn",
            "Verificar firewall/red"
        ],
        "port_error": [
            "Cambiar puerto en main_secure.py",
            "Verificar que no haya otros servicios usando el puerto",
            "Usar puerto dinámico con $PORT"
        ],
        "permission_error": [
            "Verificar permisos de archivos",
            "Revisar configuración de usuario en Dockerfile",
            "Ejecutar como root temporalmente para debug"
        ],
        "timeout_error": [
            "Aumentar timeout en railway.toml",
            "Optimizar tiempo de inicio del servicio",
            "Reducir dependencias pesadas"
        ],
        "memory_error": [
            "Reducir uso de memoria",
            "Optimizar imports",
            "Usar menos workers de uvicorn"
        ]
    }
    
    for error_type in errors_found:
        if error_type in solutions:
            print(f"\n🔧 Para {error_type}:")
            for solution in solutions[error_type]:
                print(f"   - {solution}")

def main():
    """Función principal"""
    
    # Si se proporciona archivo de log como argumento
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {log_file}")
            return 1
        except Exception as e:
            print(f"❌ Error leyendo archivo: {e}")
            return 1
    else:
        print("📋 Pegar los logs de Railway aquí (Ctrl+D para terminar):")
        log_content = sys.stdin.read()
    
    if not log_content.strip():
        print("❌ No se proporcionaron logs para analizar")
        return 1
    
    # Analizar logs
    errors_found = analyze_railway_logs(log_content)
    
    # Sugerir soluciones
    suggest_solutions(errors_found)
    
    print(f"\n📅 Análisis completado: {datetime.now()}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 