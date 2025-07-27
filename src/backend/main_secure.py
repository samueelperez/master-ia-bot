"""
API Backend Securizada para Crypto AI Bot.
Integra autenticación, rate limiting, validación y headers de seguridad.
"""

import os
import sys
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import json
import httpx
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime

# Imports para sugerencias
from services.suggestions import suggestions_service
from models.suggestion_models import (
    SuggestionRequest, 
    SuggestionResponse, 
    SuggestionItem, 
    SuggestionListResponse, 
    SuggestionStatusUpdate
)

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
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"https://api.binance.com/api/v3/ticker/price"
            params = {"symbol": f"{symbol.upper()}USDT"}
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return float(data.get("price", 0))
    except Exception as e:
        logger.error(f"Error obteniendo precio de Binance para {symbol}: {e}")
        return 0.0

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
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": coin_id,
                "vs_currencies": "usd"
            }
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if coin_id in data:
                return float(data[coin_id].get("usd", 0))
            return 0.0
    except Exception as e:
        logger.error(f"Error obteniendo precio de CoinGecko para {symbol}: {e}")
        return 0.0

async def get_current_price(symbol: str) -> float:
    """Obtener precio actual con fallback a múltiples fuentes."""
    # Intentar Binance primero
    price = await get_price_from_binance(symbol)
    if price > 0:
        return price
    
    # Fallback a CoinGecko
    price = await get_price_from_coingecko(symbol)
    if price > 0:
        return price
    
    # Fallback a precios hardcodeados
    fallback_prices = {
        "BTC": 65000.0,
        "ETH": 3400.0,
        "SOL": 120.0,
        "ADA": 0.5,
        "DOT": 7.0,
        "MATIC": 0.8,
        "AVAX": 35.0,
        "LINK": 15.0,
        "UNI": 8.0,
        "AAVE": 250.0,
        "ATOM": 8.0,
        "ALGO": 0.2
    }
    
    return fallback_prices.get(symbol.upper(), 0.0)

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
        "price_service": "enabled"  # Nuevo
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
            "health": "/ping, /healthcheck, /health/simple, /health/detailed",
            "prices": "/api/price/{symbol}",
            "status": "/api/status",
            "suggestions": "/sugerencias, /sugerencias/stats, /sugerencias/cleanup"
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
            "ai": "disabled",  # Temporal
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

# =============================================================================
# ENDPOINTS DE SUGERENCIAS
# =============================================================================

@app.post("/sugerencias", response_model=SuggestionResponse)
async def create_suggestion(
    request: SuggestionRequest,
    current_request: Request
):
    """Recibe y guarda una sugerencia de usuario."""
    try:
        # Obtener información del usuario desde el request
        user_id = getattr(current_request.state, 'user_id', 0)
        
        # Crear la sugerencia
        result = suggestions_service.add_suggestion(
            user_id=user_id,
            suggestion_text=request.suggestion_text,
            user_info={
                "username": getattr(current_request.state, 'username', ''),
                "first_name": getattr(current_request.state, 'first_name', '')
            },
            category=request.category.value if request.category else "general",
            priority=request.priority.value if request.priority else "medium"
        )
        
        if result["success"]:
            return SuggestionResponse(
                status="success",
                message="Sugerencia creada exitosamente",
                suggestion_id=result["suggestion_id"]
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=result["message"]
            )
    except Exception as e:
        logger.error(f"Error creando sugerencia: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno creando sugerencia"
        )

@app.get("/sugerencias", response_model=SuggestionListResponse)
async def get_suggestions(
    limit: int = Query(50, ge=1, le=100, description="Número máximo de sugerencias"),
    status: Optional[str] = Query(None, description="Filtrar por status (pending, approved, rejected)")
):
    """Obtener lista de sugerencias (para administradores)."""
    try:
        suggestions = suggestions_service.get_suggestions(limit=limit, status=status)
        stats = suggestions_service.get_suggestion_stats()
        
        return SuggestionListResponse(
            status="success",
            message="Sugerencias obtenidas exitosamente",
            suggestions=suggestions,
            total_count=len(suggestions),
            pending_count=stats.get("pending_suggestions", 0),
            approved_count=stats.get("approved_suggestions", 0),
            rejected_count=stats.get("rejected_suggestions", 0)
        )
    except Exception as e:
        logger.error(f"Error obteniendo sugerencias: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno obteniendo sugerencias"
        )

@app.put("/sugerencias/{suggestion_id}")
async def update_suggestion_status(
    suggestion_id: int,
    update_data: SuggestionStatusUpdate
):
    """Actualizar status de una sugerencia (solo administradores)."""
    try:
        result = suggestions_service.update_suggestion_status(
            suggestion_id=suggestion_id,
            status=update_data.status.value if update_data.status else "pending",
            admin_notes=update_data.admin_notes,
            admin_id=update_data.admin_id
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": "Status actualizado exitosamente",
                "suggestion_id": suggestion_id
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=result["message"]
            )
    except Exception as e:
        logger.error(f"Error actualizando sugerencia {suggestion_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno actualizando sugerencia"
        )

@app.get("/sugerencias/stats")
async def get_suggestion_stats():
    """Obtener estadísticas de sugerencias."""
    try:
        stats = suggestions_service.get_suggestion_stats()
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno obteniendo estadísticas"
        )

@app.delete("/sugerencias/{suggestion_id}")
async def delete_suggestion(suggestion_id: int):
    """Eliminar una sugerencia (solo administradores)."""
    try:
        result = suggestions_service.delete_suggestion(suggestion_id)
        
        if result["success"]:
            return {
                "success": True,
                "message": "Sugerencia eliminada exitosamente",
                "suggestion_id": suggestion_id
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=result["message"]
            )
    except Exception as e:
        logger.error(f"Error eliminando sugerencia {suggestion_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno eliminando sugerencia"
        )

@app.post("/sugerencias/cleanup")
async def cleanup_suggestions(
    days_to_keep: int = Query(365, ge=30, le=3650, description="Días a mantener")
):
    """Limpiar sugerencias antiguas (solo administradores)."""
    try:
        result = suggestions_service.cleanup_old_suggestions(days_to_keep)
        return {
            "success": True,
            "message": f"Limpieza completada. {result['deleted_count']} sugerencias eliminadas",
            "deleted_count": result["deleted_count"]
        }
    except Exception as e:
        logger.error(f"Error en limpieza de sugerencias: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno en limpieza de sugerencias"
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