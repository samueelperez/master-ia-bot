"""
Modelos Pydantic para el sistema de sugerencias
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, validator
from datetime import datetime


class SuggestionRequest(BaseModel):
    """Modelo para solicitud de nueva sugerencia."""
    suggestion: str
    user_info: Optional[Dict[str, Any]] = None
    
    @validator('suggestion')
    def validate_suggestion(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('La sugerencia no puede estar vacía')
        if len(v) > 1000:
            raise ValueError('La sugerencia no puede exceder 1000 caracteres')
        return v.strip()


class SuggestionItem(BaseModel):
    """Modelo para un item de sugerencia."""
    id: int
    user_id: str
    suggestion_text: str
    user_info: Optional[Dict[str, Any]] = None
    status: str
    admin_notes: Optional[str] = None
    created_at: str
    updated_at: str


class SuggestionResponse(BaseModel):
    """Modelo para respuesta de sugerencia."""
    status: str
    message: str
    suggestion_id: Optional[int] = None


class SuggestionListResponse(BaseModel):
    """Modelo para lista de sugerencias."""
    suggestions: List[SuggestionItem]
    total: int
    limit: int


class SuggestionStatusUpdate(BaseModel):
    """Modelo para actualización de status de sugerencia."""
    status: str
    admin_notes: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['pending', 'approved', 'rejected', 'in_progress']
        if v not in valid_statuses:
            raise ValueError(f'Status debe ser uno de: {", ".join(valid_statuses)}')
        return v


class SuggestionFilter(BaseModel):
    """Modelo para filtros de sugerencias."""
    status: Optional[str] = None
    user_id: Optional[str] = None
    limit: int = 50
    offset: int = 0
    
    @validator('limit')
    def validate_limit(cls, v):
        if v < 1 or v > 100:
            raise ValueError('Limit debe estar entre 1 y 100')
        return v
    
    @validator('offset')
    def validate_offset(cls, v):
        if v < 0:
            raise ValueError('Offset no puede ser negativo')
        return v 