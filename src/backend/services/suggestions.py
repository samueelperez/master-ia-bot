"""
Servicio de Sugerencias para Crypto AI Bot
Gestiona sugerencias de usuarios para mejorar el sistema
"""

import json
import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SuggestionsService:
    """Servicio para gestionar sugerencias de usuarios."""
    
    def __init__(self, db_path: str = "suggestions.db"):
        """Inicializar el servicio de sugerencias."""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Inicializar la base de datos SQLite para sugerencias."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Crear tabla de sugerencias si no existe
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS suggestions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    suggestion_text TEXT NOT NULL,
                    user_info TEXT,
                    status TEXT DEFAULT 'pending',
                    admin_notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Verificar si la columna user_info existe, si no, agregarla
            try:
                cursor.execute('SELECT user_info FROM suggestions LIMIT 1')
            except sqlite3.OperationalError:
                logger.info("🔄 Agregando columna user_info a la tabla suggestions...")
                cursor.execute('ALTER TABLE suggestions ADD COLUMN user_info TEXT')
            
            conn.commit()
            conn.close()
            logger.info("✅ Base de datos de sugerencias inicializada correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error inicializando base de datos de sugerencias: {e}")
    
    def add_suggestion(self, user_id: str, suggestion_text: str, user_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Agregar una nueva sugerencia."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convertir user_info a JSON string
            user_info_json = json.dumps(user_info) if user_info else None
            
            cursor.execute('''
                INSERT INTO suggestions (user_id, suggestion_text, user_info, status)
                VALUES (?, ?, ?, 'pending')
            ''', (user_id, suggestion_text, user_info_json))
            
            suggestion_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Sugerencia agregada - ID: {suggestion_id}, User: {user_id}")
            
            return {
                "status": "success",
                "message": "Sugerencia enviada correctamente",
                "suggestion_id": suggestion_id
            }
            
        except Exception as e:
            logger.error(f"❌ Error agregando sugerencia: {e}")
            return {
                "status": "error",
                "message": "Error interno del servidor"
            }
    
    def get_suggestions(self, limit: int = 50, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener lista de sugerencias."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if status:
                cursor.execute('''
                    SELECT id, user_id, suggestion_text, user_info, status, admin_notes, created_at, updated_at
                    FROM suggestions 
                    WHERE status = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (status, limit))
            else:
                cursor.execute('''
                    SELECT id, user_id, suggestion_text, user_info, status, admin_notes, created_at, updated_at
                    FROM suggestions 
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (limit,))
            
            suggestions = []
            for row in cursor.fetchall():
                suggestion = {
                    "id": row[0],
                    "user_id": row[1],
                    "suggestion_text": row[2],
                    "user_info": json.loads(row[3]) if row[3] else None,
                    "status": row[4],
                    "admin_notes": row[5],
                    "created_at": row[6],
                    "updated_at": row[7]
                }
                suggestions.append(suggestion)
            
            conn.close()
            logger.info(f"✅ Obtenidas {len(suggestions)} sugerencias")
            
            return suggestions
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo sugerencias: {e}")
            return []
    
    def update_suggestion_status(self, suggestion_id: int, status: str, admin_notes: str = None) -> Dict[str, Any]:
        """Actualizar el status de una sugerencia."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE suggestions 
                SET status = ?, admin_notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, admin_notes, suggestion_id))
            
            if cursor.rowcount == 0:
                conn.close()
                return {
                    "status": "error",
                    "message": "Sugerencia no encontrada"
                }
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Sugerencia {suggestion_id} actualizada a status: {status}")
            
            return {
                "status": "success",
                "message": "Sugerencia actualizada correctamente",
                "suggestion_id": suggestion_id,
                "new_status": status
            }
            
        except Exception as e:
            logger.error(f"❌ Error actualizando sugerencia {suggestion_id}: {e}")
            return {
                "status": "error",
                "message": "Error interno del servidor"
            }
    
    def get_suggestion_by_id(self, suggestion_id: int) -> Optional[Dict[str, Any]]:
        """Obtener una sugerencia específica por ID."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, user_id, suggestion_text, user_info, status, admin_notes, created_at, updated_at
                FROM suggestions 
                WHERE id = ?
            ''', (suggestion_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    "id": row[0],
                    "user_id": row[1],
                    "suggestion_text": row[2],
                    "user_info": json.loads(row[3]) if row[3] else None,
                    "status": row[4],
                    "admin_notes": row[5],
                    "created_at": row[6],
                    "updated_at": row[7]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo sugerencia {suggestion_id}: {e}")
            return None
    
    def delete_suggestion(self, suggestion_id: int) -> Dict[str, Any]:
        """Eliminar una sugerencia."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM suggestions WHERE id = ?', (suggestion_id,))
            
            if cursor.rowcount == 0:
                conn.close()
                return {
                    "status": "error",
                    "message": "Sugerencia no encontrada"
                }
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Sugerencia {suggestion_id} eliminada")
            
            return {
                "status": "success",
                "message": "Sugerencia eliminada correctamente"
            }
            
        except Exception as e:
            logger.error(f"❌ Error eliminando sugerencia {suggestion_id}: {e}")
            return {
                "status": "error",
                "message": "Error interno del servidor"
            }

# Instancia global del servicio
suggestions_service = SuggestionsService() 