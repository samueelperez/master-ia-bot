#!/usr/bin/env python3
"""
Script para probar el endpoint /ping del backend
"""

import requests
import time
import sys

def test_ping_endpoint():
    """Prueba el endpoint /ping del backend"""
    
    # URLs a probar
    urls = [
        "http://localhost:8000/ping",
        "http://127.0.0.1:8000/ping",
        "http://0.0.0.0:8000/ping"
    ]
    
    print("🔍 Probando endpoint /ping...")
    
    for url in urls:
        try:
            print(f"📡 Probando: {url}")
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {url} - Status: {response.status_code}")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ {url} - Status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {url} - Connection Error (servicio no disponible)")
        except requests.exceptions.Timeout:
            print(f"❌ {url} - Timeout")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")
    
    return False

def test_health_endpoint():
    """Prueba el endpoint /health del backend"""
    
    urls = [
        "http://localhost:8000/health",
        "http://127.0.0.1:8000/health",
        "http://0.0.0.0:8000/health"
    ]
    
    print("\n🔍 Probando endpoint /health...")
    
    for url in urls:
        try:
            print(f"📡 Probando: {url}")
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {url} - Status: {response.status_code}")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ {url} - Status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {url} - Connection Error (servicio no disponible)")
        except requests.exceptions.Timeout:
            print(f"❌ {url} - Timeout")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")
    
    return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de endpoints...")
    print("=" * 50)
    
    # Probar /ping
    ping_ok = test_ping_endpoint()
    
    # Probar /health
    health_ok = test_health_endpoint()
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS:")
    print(f"/ping: {'✅ FUNCIONA' if ping_ok else '❌ NO FUNCIONA'}")
    print(f"/health: {'✅ FUNCIONA' if health_ok else '❌ NO FUNCIONA'}")
    
    if ping_ok:
        print("\n🎉 El endpoint /ping está funcionando correctamente!")
        print("✅ Railway debería poder hacer healthcheck exitosamente")
        return 0
    else:
        print("\n⚠️ El endpoint /ping no está funcionando")
        print("❌ Railway no podrá hacer healthcheck")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 