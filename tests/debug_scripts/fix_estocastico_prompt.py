#!/usr/bin/env python3
"""
Script para probar un prompt mejorado del estocástico.
"""

import asyncio
import httpx
import json

# Configuración
AI_MODULE_URL = "http://localhost:8001"
AUTH_TOKEN = "cr1nW3IDA-CQlkm6XBIoIdZmqv9mLj6U_-1z0ttyOZ4"

# Prompt mejorado para el estocástico
IMPROVED_ESTOCASTICO_PROMPT = '''Eres un analista técnico experto en el indicador Estocástico. Analiza los datos OHLCV proporcionados para {activo} en {timeframe}.

DATOS TÉCNICOS ACTUALES:
{datos_tecnicos}

INSTRUCCIONES ESTRICTAS:
1. Analiza ÚNICAMENTE los datos OHLCV proporcionados.
2. Para detectar señales del Estocástico, necesitas calcular %K y %D:
   - %K = ((Precio actual - Mínimo más bajo) / (Máximo más alto - Mínimo más bajo)) * 100
   - %D = Media móvil de %K (típicamente 3 períodos)

3. CRITERIOS PARA SEÑAL VÁLIDA:
   - %K > 80 y %K cruza %D hacia abajo = SEÑAL SHORT
   - %K < 20 y %K cruza %D hacia arriba = SEÑAL LONG
   - Divergencia entre precio y Estocástico

4. RESPUESTA OBLIGATORIA:
   Si NO puedes calcular %K/%D con los datos proporcionados o no hay señal clara, responde EXACTAMENTE:
   "No hay señal de entrada clara según el Estocástico en estos datos."

   Si SÍ hay señal clara, responde en este formato:
   - Dirección: LONG/SHORT
   - Señal técnica: [descripción específica]
   - Punto de entrada: $[precio de los datos]
   - Stop loss: $[precio de los datos]
   - Take profit: $[precio de los datos]

NO inventes datos. NO generes señales sin evidencia técnica clara.'''

async def test_improved_prompt():
    """Probar el prompt mejorado."""
    print("🧪 Probando prompt mejorado del estocástico...")
    
    try:
        # Simular el payload que enviaría el servicio
        payload = {
            "strategy_type": "estocastico",
            "symbol": "BTC",
            "timeframe": "5m",
            "user_prompt": "Dame una señal de scalping estocástico para BTC en 5m",
            "include_risk_analysis": True,
            "include_price_targets": True
        }
        
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AI_MODULE_URL}/advanced-strategy",
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                reasoning = result.get('result', {}).get('reasoning', 'N/A')
                signal = result.get('result', {}).get('signal', 'N/A')
                
                print(f"📊 Respuesta actual:")
                print(f"   - Señal: {signal}")
                print(f"   - Razón: {reasoning}")
                
                # Verificar si hay contradicción
                if "no hay señal" in reasoning.lower() and ("$" in reasoning or "entrada" in reasoning.lower()):
                    print("❌ PROBLEMA: Respuesta contradictoria detectada")
                    return False
                else:
                    print("✅ Respuesta coherente")
                    return True
            else:
                print(f"❌ Error {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

async def main():
    """Función principal."""
    print("🔧 CORRECCIÓN DE PROMPT DEL ESTOCÁSTICO")
    print("=" * 60)
    
    success = await test_improved_prompt()
    
    if success:
        print("\n✅ El prompt actual funciona correctamente")
    else:
        print("\n⚠️  El prompt necesita mejoras")
        print("\n💡 Recomendaciones:")
        print("1. Hacer el prompt más específico sobre calcular %K/%D")
        print("2. Forzar respuestas binarias (señal o no señal)")
        print("3. Evitar que el modelo genere análisis sin datos suficientes")

if __name__ == "__main__":
    asyncio.run(main()) 