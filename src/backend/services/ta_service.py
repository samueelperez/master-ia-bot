# import pandas as pd  # Comentado temporalmente para compatibilidad con Python 3.13
import logging
from typing import Dict, List, Optional, Any
import json

logger = logging.getLogger(__name__)

# Configuración temporal sin pandas
INDICATOR_PROFILES = {
    "basic": {
        "description": "Indicadores básicos para principiantes",
        "indicators": ["sma", "ema", "rsi", "macd"]
    },
    "intermediate": {
        "description": "Indicadores intermedios para traders experimentados",
        "indicators": ["bollinger_bands", "stochastic", "atr", "volume_sma"]
    },
    "advanced": {
        "description": "Indicadores avanzados para traders expertos",
        "indicators": ["fibonacci", "pivot_points", "support_resistance", "volume_profile"]
    }
}

def get_available_indicators() -> Dict[str, List[str]]:
    """Obtener indicadores disponibles (versión simplificada sin pandas)."""
    return {
        "trend": ["sma", "ema", "macd", "bollinger_bands"],
        "momentum": ["rsi", "stochastic", "williams_r"],
        "volatility": ["atr", "bollinger_bands", "keltner_channels"],
        "volume": ["volume_sma", "volume_profile", "obv"],
        "support_resistance": ["pivot_points", "fibonacci", "support_resistance"],
        "patterns": ["doji", "hammer", "engulfing", "shooting_star"]
    }

def calculate_indicators(data: List[Dict], indicators: List[str]) -> Dict[str, Any]:
    """Calcular indicadores (versión simplificada sin pandas)."""
    logger.warning("⚠️ Funcionalidad de indicadores deshabilitada temporalmente")
    return {
        "status": "disabled",
        "message": "Indicadores técnicos temporalmente deshabilitados para compatibilidad",
        "data": data[:10] if data else []  # Retornar solo los primeros 10 datos
    }

def get_indicator_profile(profile: str) -> Dict[str, Any]:
    """Obtener perfil de indicadores."""
    return INDICATOR_PROFILES.get(profile, INDICATOR_PROFILES["basic"])
