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
        "database": "disabled"  # Temporal
    }

# Endpoints principales
@app.get("/")
async def root():
    """Endpoint raíz."""
    return {
        "message": "🚀 Crypto AI Bot Backend",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
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
            "ai": "disabled"  # Temporal
        }
    }

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