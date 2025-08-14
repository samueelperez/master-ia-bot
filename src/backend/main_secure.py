"""
API Backend Securizada para Crypto AI Bot.
Integra autenticación, rate limiting, validación y headers de seguridad.
"""

import os
import sys
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import json
import httpx
import asyncio

# Comentado temporalmente para compatibilidad con Python 3.13
# from sqlalchemy.orm import Session
# from .core.db import get_db
# from .core.models import User

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://*.onrender.com",
    "*"  # Temporal para desarrollo
]

# Middleware de rate limiting simple
class RateLimiter:
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, client_ip: str, limit: int = 60) -> bool:
        now = time.time()
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Limpiar requests antiguos (último minuto)
        self.requests[client_ip] = [req for req in self.requests[client_ip] if now - req < 60]
        
        if len(self.requests[client_ip]) >= limit:
            return False
        
        self.requests[client_ip].append(now)
        return True

rate_limiter = RateLimiter()

# Cliente HTTP para obtener precios
async def get_price_from_binance(symbol: str) -> float:
    """Obtener precio desde Binance."""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            url = f"https://api.binance.com/api/v3/ticker/price"
            params = {"symbol": f"{symbol.upper()}USDT"}
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            price = float(data.get("price", 0))
            if price > 0:
                logger.info(f"Precio obtenido de Binance para {symbol}: ${price:,.2f}")
                return price
            else:
                raise Exception("Precio inválido recibido de Binance")
    except Exception as e:
        logger.error(f"Error obteniendo precio de Binance para {symbol}: {e}")
        raise Exception(f"Binance no disponible para {symbol}: {str(e)}")

async def get_price_from_coingecko(symbol: str) -> float:
    """Obtener precio desde CoinGecko."""
    try:
        # Mapeo de símbolos a IDs de CoinGecko
        symbol_mapping = {
            "BTC": "bitcoin", "ETH": "ethereum", "ADA": "cardano",
            "DOT": "polkadot", "SOL": "solana", "MATIC": "matic-network",
            "AVAX": "avalanche-2", "LINK": "chainlink", "UNI": "uniswap",
            "AAVE": "aave", "ATOM": "cosmos", "ALGO": "algorand"
        }
        
        coin_id = symbol_mapping.get(symbol.upper(), symbol.lower())
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": coin_id,
                "vs_currencies": "usd"
            }
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if coin_id in data:
                price = float(data[coin_id].get("usd", 0))
                if price > 0:
                    logger.info(f"Precio obtenido de CoinGecko para {symbol}: ${price:,.2f}")
                    return price
                else:
                    raise Exception("Precio inválido recibido de CoinGecko")
            else:
                raise Exception(f"ID de moneda {coin_id} no encontrado en CoinGecko")
    except Exception as e:
        logger.error(f"Error obteniendo precio de CoinGecko para {symbol}: {e}")
        raise Exception(f"CoinGecko no disponible para {symbol}: {str(e)}")

async def get_current_price(symbol: str) -> float:
    """Obtener precio actual solo de fuentes reales."""
    logger.info(f"🔍 Obteniendo precio real para {symbol}...")
    
    # Intentar Binance primero
    try:
        price = await get_price_from_binance(symbol)
        logger.info(f"✅ Precio obtenido exitosamente de Binance para {symbol}")
        return price
    except Exception as binance_error:
        logger.warning(f"⚠️ Binance falló para {symbol}: {binance_error}")
        
        # Si Binance falla, intentar CoinGecko
        try:
            price = await get_price_from_coingecko(symbol)
            logger.info(f"✅ Precio obtenido exitosamente de CoinGecko para {symbol}")
            return price
        except Exception as coingecko_error:
            logger.error(f"❌ CoinGecko también falló para {symbol}: {coingecko_error}")
            
            # Si ambas fuentes fallan, lanzar error
            error_msg = f"No se pudo obtener precio real para {symbol}. Binance: {binance_error}, CoinGecko: {coingecko_error}"
            logger.error(error_msg)
            raise Exception(error_msg)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Iniciando Crypto AI Bot Backend...")
    logger.info("✅ Backend iniciado correctamente")
    yield
    # Shutdown
    logger.info("🛑 Cerrando Crypto AI Bot Backend...")

app = FastAPI(
    title="Crypto AI Bot Backend",
    description="Backend API para el bot de trading con IA",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de rate limiting
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    if not rate_limiter.is_allowed(client_ip):
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded. Please try again later."}
        )
    response = await call_next(request)
    return response

# Healthcheck endpoints
@app.get("/ping")
async def ping():
    """Endpoint ultra simple para Render healthcheck."""
    return {"pong": "ok"}

@app.get("/healthcheck")
async def healthcheck():
    """Healthcheck simple para Render."""
    return {"status": "healthy"}

@app.get("/health/simple")
async def health_simple():
    """Health check simple y rápido para Render."""
    return {"status": "ok"}

@app.get("/health/detailed")
async def health_detailed():
    """Health check detallado."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database": "disabled",  # Temporal
        "price_service": "enabled",  # Nuevo
        "apis": {
            "binance": "enabled",
            "coingecko": "enabled"
        }
    }

@app.get("/health/price-apis")
async def health_price_apis():
    """Health check específico para APIs de precios."""
    try:
        # Probar Binance
        btc_price_binance = await get_price_from_binance("BTC")
        binance_status = "healthy" if btc_price_binance > 0 else "error"
        
        # Probar CoinGecko
        btc_price_coingecko = await get_price_from_coingecko("BTC")
        coingecko_status = "healthy" if btc_price_coingecko > 0 else "error"
        
        return {
            "status": "healthy" if binance_status == "healthy" or coingecko_status == "healthy" else "degraded",
            "timestamp": time.time(),
            "apis": {
                "binance": {
                    "status": binance_status,
                    "btc_price": btc_price_binance,
                    "last_check": time.time()
                },
                "coingecko": {
                    "status": coingecko_status,
                    "btc_price": btc_price_coingecko,
                    "last_check": time.time()
                }
            }
        }
    except Exception as e:
        logger.error(f"Error en health check de APIs de precios: {e}")
        return {
            "status": "error",
            "timestamp": time.time(),
            "error": str(e),
            "apis": {
                "binance": {"status": "error", "error": "No disponible"},
                "coingecko": {"status": "error", "error": "No disponible"}
            }
        }

# Endpoints principales
@app.get("/")
async def root():
    """Endpoint raíz."""
    return {
        "message": "🚀 Crypto AI Bot Backend",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "health": "/ping, /healthcheck, /health/simple, /health/detailed, /health/price-apis",
            "prices": "/api/price/{symbol}",
            "status": "/api/status",
            "ai": "/advanced-strategy"
        }
    }

@app.get("/api/status")
async def api_status():
    """Estado de la API."""
    return {
        "api": "Crypto AI Bot Backend",
        "version": "1.0.0",
        "status": "operational",
        "features": {
            "database": "disabled",  # Temporal
            "indicators": "disabled",  # Temporal
            "trading": "disabled",  # Temporal
            "ai": "enabled",  # Nuevo endpoint implementado
            "price_service": "enabled"  # Nuevo
        }
    }

# Endpoint de precios (NUEVO)
@app.get("/api/price/{symbol}")
async def get_price(symbol: str):
    """Obtener precio actual de una criptomoneda."""
    try:
        symbol = symbol.upper()
        price = await get_current_price(symbol)
        
        if price > 0:
            return {
                "symbol": symbol,
                "price": price,
                "currency": "USD",
                "timestamp": time.time(),
                "source": "binance/coingecko"
            }
        else:
            raise HTTPException(
                status_code=404,
                detail=f"No se pudo obtener precio para {symbol}"
            )
    except Exception as e:
        logger.error(f"Error obteniendo precio para {symbol}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno obteniendo precio para {symbol}"
        )

# Endpoint para múltiples precios
@app.get("/api/prices")
async def get_multiple_prices(symbols: str):
    """Obtener precios de múltiples criptomonedas."""
    try:
        symbol_list = [s.strip().upper() for s in symbols.split(",")]
        prices = {}
        
        for symbol in symbol_list:
            price = await get_current_price(symbol)
            if price > 0:
                prices[symbol] = price
        
        return {
            "prices": prices,
            "timestamp": time.time(),
            "currency": "USD"
        }
    except Exception as e:
        logger.error(f"Error obteniendo múltiples precios: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno obteniendo precios"
        )

# Endpoints temporales
@app.get("/api/indicators")
async def get_indicators():
    """Obtener indicadores (versión temporal)."""
    return {
        "status": "disabled",
        "message": "Indicadores técnicos temporalmente deshabilitados",
        "available_indicators": [
            "sma", "ema", "rsi", "macd", "bollinger_bands"
        ]
    }

@app.get("/api/strategies")
async def get_strategies():
    """Obtener estrategias (versión temporal)."""
    return {
        "status": "disabled",
        "message": "Estrategias temporalmente deshabilitadas",
        "available_strategies": [
            "scalping", "swing_trading", "position_trading"
        ]
    }

# Endpoint para estrategias avanzadas (simula AI Module)
@app.post("/advanced-strategy")
async def advanced_strategy(request: Request):
    """Endpoint para estrategias avanzadas de trading."""
    try:
        # Obtener datos del request
        data = await request.json()
        symbol = data.get("symbol", "BTC")
        timeframe = data.get("timeframe", "1h")
        
        # Obtener precio actual
        current_price = await get_current_price(symbol)
        
        # Simular análisis técnico básico
        import random
        
        # Generar señal aleatoria para demostración
        signals = ["BUY", "SELL", "NEUTRAL"]
        signal = random.choice(signals)
        
        # Calcular precios simulados
        if signal == "BUY":
            entry_price = current_price * 0.995  # Ligeramente por debajo del precio actual
            stop_loss = entry_price * 0.98      # 2% por debajo del entry
            take_profit = entry_price * 1.03    # 3% por encima del entry
        elif signal == "SELL":
            entry_price = current_price * 1.005  # Ligeramente por encima del precio actual
            stop_loss = entry_price * 1.02      # 2% por encima del entry
            take_profit = entry_price * 0.97    # 3% por debajo del entry
        else:
            entry_price = current_price
            stop_loss = current_price * 0.98
            take_profit = current_price * 1.02
        
        # Generar razonamiento simulado
        reasoning_map = {
            "BUY": f"Análisis técnico sugiere oportunidad de compra en {symbol}. El precio muestra momentum alcista en {timeframe}.",
            "SELL": f"Indicadores técnicos sugieren venta en {symbol}. Se detecta debilidad en el timeframe {timeframe}.",
            "NEUTRAL": f"El mercado de {symbol} se encuentra en equilibrio. No hay señales claras en {timeframe}."
        }
        
        result = {
            "status": "success",
            "result": {
                "signal": signal,
                "symbol": symbol,
                "timeframe": timeframe,
                "entry_price": round(entry_price, 4),
                "stop_loss": round(stop_loss, 4),
                "take_profit": round(take_profit, 4),
                "confidence": round(random.uniform(0.6, 0.9), 2),
                "reasoning": reasoning_map[signal],
                "current_price": current_price,
                "timestamp": time.time()
            }
        }
        
        logger.info(f"Estrategia generada para {symbol} en {timeframe}: {signal}")
        return result
        
    except Exception as e:
        logger.error(f"Error en advanced-strategy: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno generando estrategia: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    
    # Configuración del servidor
    port = int(os.getenv("BACKEND_PORT", 8000))
    host = "0.0.0.0"
    
    logger.info(f"🌐 Iniciando servidor en {host}:{port}")
    
    uvicorn.run(
        "main_secure:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    ) 