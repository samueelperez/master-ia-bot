from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class SuggestionCategory(str, Enum):
    IMPROVEMENT = "improvement"
    BUG = "bug"
    FEATURE = "feature"
    FEEDBACK = "feedback"
    GENERAL = "general"

class SuggestionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"

class SuggestionPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class SuggestionRequest(BaseModel):
    suggestion_text: str = Field(..., min_length=1, max_length=2000, description="Texto de la sugerencia")
    category: Optional[SuggestionCategory] = Field(default=SuggestionCategory.GENERAL, description="Categoría de la sugerencia")
    priority: Optional[SuggestionPriority] = Field(default=SuggestionPriority.MEDIUM, description="Prioridad de la sugerencia")
    
    @validator('suggestion_text')
    def validate_suggestion_text(cls, v):
        if not v.strip():
            raise ValueError('El texto de la sugerencia no puede estar vacío')
        return v.strip()

class SuggestionResponse(BaseModel):
    status: str = Field(..., description="Estado de la operación")
    message: str = Field(..., description="Mensaje descriptivo")
    suggestion_id: Optional[int] = Field(None, description="ID de la sugerencia creada")

class SuggestionItem(BaseModel):
    id: int = Field(..., description="ID único de la sugerencia")
    user_id: int = Field(..., description="ID del usuario que creó la sugerencia")
    username: Optional[str] = Field(None, description="Username del usuario")
    first_name: Optional[str] = Field(None, description="Nombre del usuario")
    suggestion_text: str = Field(..., description="Texto de la sugerencia")
    category: SuggestionCategory = Field(..., description="Categoría de la sugerencia")
    status: SuggestionStatus = Field(..., description="Estado actual de la sugerencia")
    priority: SuggestionPriority = Field(..., description="Prioridad de la sugerencia")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")
    admin_notes: Optional[str] = Field(None, description="Notas del administrador")
    admin_id: Optional[int] = Field(None, description="ID del administrador que procesó la sugerencia")

class SuggestionListResponse(BaseModel):
    status: str = Field(..., description="Estado de la operación")
    message: str = Field(..., description="Mensaje descriptivo")
    suggestions: List[SuggestionItem] = Field(..., description="Lista de sugerencias")
    total_count: int = Field(..., description="Total de sugerencias")
    pending_count: int = Field(..., description="Sugerencias pendientes")
    approved_count: int = Field(..., description="Sugerencias aprobadas")
    rejected_count: int = Field(..., description="Sugerencias rechazadas")

class SuggestionStatusUpdate(BaseModel):
    status: SuggestionStatus = Field(..., description="Nuevo estado de la sugerencia")
    admin_notes: Optional[str] = Field(None, max_length=1000, description="Notas del administrador")
    admin_id: Optional[int] = Field(None, description="ID del administrador")
    
    @validator('admin_notes')
    def validate_admin_notes(cls, v):
        if v is not None and not v.strip():
            return None
        return v.strip() if v else None

class SuggestionStats(BaseModel):
    total_suggestions: int = Field(..., description="Total de sugerencias")
    pending_suggestions: int = Field(..., description="Sugerencias pendientes")
    approved_suggestions: int = Field(..., description="Sugerencias aprobadas")
    rejected_suggestions: int = Field(..., description="Sugerencias rechazadas")
    in_progress_suggestions: int = Field(..., description="Sugerencias en progreso")
    recent_suggestions: int = Field(..., description="Sugerencias de los últimos 7 días")
    top_categories: dict = Field(..., description="Categorías más populares")
    top_priorities: dict = Field(..., description="Prioridades más comunes") 