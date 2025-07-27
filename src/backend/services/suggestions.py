import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SuggestionsService:
    """
    Servicio para gestionar sugerencias de usuarios con SQLite.
    Incluye operaciones CRUD completas y estadísticas.
    """
    
    def __init__(self, db_path: str = "suggestions.db"):
        """Inicializa el servicio de sugerencias."""
        self.db_path = db_path
        self.connection_timeout = 30
        self._init_db()
        logger.info(f"SuggestionsService inicializado con BD: {self.db_path}")
    
    @contextmanager
    def _get_connection(self):
        """Context manager para conexiones seguras a la base de datos."""
        conn = None
        try:
            conn = sqlite3.connect(
                self.db_path, 
                timeout=self.connection_timeout,
                check_same_thread=False
            )
            conn.execute("PRAGMA foreign_keys = ON")
            conn.row_factory = sqlite3.Row  # Para acceso por nombre de columna
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Error de base de datos: {str(e)}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    def _init_db(self):
        """Inicializa la base de datos con constraints de seguridad."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla principal de sugerencias
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS suggestions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL CHECK(user_id > 0),
                    username TEXT CHECK(length(username) <= 100),
                    first_name TEXT CHECK(length(first_name) <= 100),
                    suggestion_text TEXT NOT NULL CHECK(length(suggestion_text) <= 2000),
                    category TEXT CHECK(category IN ('improvement', 'bug', 'feature', 'feedback', 'general')) DEFAULT 'general',
                    status TEXT CHECK(status IN ('pending', 'approved', 'rejected', 'in_progress')) DEFAULT 'pending',
                    priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'urgent')) DEFAULT 'medium',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    admin_notes TEXT CHECK(length(admin_notes) <= 1000),
                    admin_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                )
            ''')
            
            # Tabla de usuarios (si no existe)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY CHECK(user_id > 0),
                    username TEXT CHECK(length(username) <= 100),
                    first_name TEXT CHECK(length(first_name) <= 100),
                    last_name TEXT CHECK(length(last_name) <= 100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Índices para rendimiento
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_suggestions_status ON suggestions(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_suggestions_user ON suggestions(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_suggestions_created ON suggestions(created_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_suggestions_category ON suggestions(category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_suggestions_priority ON suggestions(priority)")
            
            conn.commit()
            logger.info("Base de datos de sugerencias inicializada correctamente")
    
    def _ensure_user_exists(self, user_id: int, username: str = None, first_name: str = None) -> bool:
        """Asegura que el usuario existe en la tabla de usuarios."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar si el usuario existe
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            if cursor.fetchone():
                # Actualizar información si es necesario
                if username or first_name:
                    cursor.execute('''
                        UPDATE users 
                        SET username = COALESCE(?, username), 
                            first_name = COALESCE(?, first_name),
                            last_active = ?
                        WHERE user_id = ?
                    ''', (username, first_name, datetime.now(), user_id))
                return True
            
            # Crear usuario si no existe
            cursor.execute('''
                INSERT INTO users (user_id, username, first_name, created_at, last_active)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, datetime.now(), datetime.now()))
            
            conn.commit()
            return True
    
    def add_suggestion(self, user_id: int, suggestion_text: str, user_info: dict = None, 
                      category: str = "general", priority: str = "medium") -> Dict[str, Any]:
        """Agrega una nueva sugerencia."""
        try:
            # Validar entrada
            if not suggestion_text.strip():
                return {"status": "error", "message": "El texto de la sugerencia no puede estar vacío"}
            
            if len(suggestion_text) > 2000:
                return {"status": "error", "message": "La sugerencia es demasiado larga (máximo 2000 caracteres)"}
            
            # Extraer información del usuario
            username = user_info.get('username', '') if user_info else ''
            first_name = user_info.get('first_name', '') if user_info else ''
            
            # Asegurar que el usuario existe
            self._ensure_user_exists(user_id, username, first_name)
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO suggestions (
                        user_id, username, first_name, suggestion_text, 
                        category, priority, created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id, username, first_name, suggestion_text.strip(),
                    category, priority, datetime.now(), datetime.now()
                ))
                
                suggestion_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"Sugerencia creada: ID={suggestion_id}, User={user_id}")
                
                return {
                    "status": "success",
                    "message": "Sugerencia creada exitosamente",
                    "suggestion_id": suggestion_id
                }
                
        except Exception as e:
            logger.error(f"Error al crear sugerencia: {str(e)}")
            return {"status": "error", "message": f"Error interno: {str(e)}"}
    
    def get_suggestions(self, limit: int = 50, status: str = None, 
                       category: str = None, user_id: int = None) -> List[Dict[str, Any]]:
        """Obtiene sugerencias con filtros opcionales."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM suggestions WHERE 1=1"
                params = []
                
                if status:
                    query += " AND status = ?"
                    params.append(status)
                
                if category:
                    query += " AND category = ?"
                    params.append(category)
                
                if user_id:
                    query += " AND user_id = ?"
                    params.append(user_id)
                
                query += " ORDER BY created_at DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                suggestions = []
                for row in rows:
                    suggestions.append({
                        "id": row['id'],
                        "user_id": row['user_id'],
                        "username": row['username'],
                        "first_name": row['first_name'],
                        "suggestion_text": row['suggestion_text'],
                        "category": row['category'],
                        "status": row['status'],
                        "priority": row['priority'],
                        "created_at": row['created_at'],
                        "updated_at": row['updated_at'],
                        "admin_notes": row['admin_notes'],
                        "admin_id": row['admin_id']
                    })
                
                return suggestions
                
        except Exception as e:
            logger.error(f"Error al obtener sugerencias: {str(e)}")
            return []
    
    def get_suggestion_by_id(self, suggestion_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una sugerencia específica por ID."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM suggestions WHERE id = ?", (suggestion_id,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        "id": row['id'],
                        "user_id": row['user_id'],
                        "username": row['username'],
                        "first_name": row['first_name'],
                        "suggestion_text": row['suggestion_text'],
                        "category": row['category'],
                        "status": row['status'],
                        "priority": row['priority'],
                        "created_at": row['created_at'],
                        "updated_at": row['updated_at'],
                        "admin_notes": row['admin_notes'],
                        "admin_id": row['admin_id']
                    }
                
                return None
                
        except Exception as e:
            logger.error(f"Error al obtener sugerencia {suggestion_id}: {str(e)}")
            return None
    
    def update_suggestion_status(self, suggestion_id: int, status: str, 
                               admin_notes: str = None, admin_id: int = None) -> Dict[str, Any]:
        """Actualiza el estado de una sugerencia."""
        try:
            # Validar estado
            valid_statuses = ['pending', 'approved', 'rejected', 'in_progress']
            if status not in valid_statuses:
                return {"status": "error", "message": f"Estado inválido. Debe ser uno de: {', '.join(valid_statuses)}"}
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE suggestions 
                    SET status = ?, admin_notes = ?, admin_id = ?, updated_at = ?
                    WHERE id = ?
                ''', (status, admin_notes, admin_id, datetime.now(), suggestion_id))
                
                if cursor.rowcount == 0:
                    return {"status": "error", "message": "Sugerencia no encontrada"}
                
                conn.commit()
                
                logger.info(f"Sugerencia {suggestion_id} actualizada a estado: {status}")
                
                return {"status": "success", "message": "Estado actualizado exitosamente"}
                
        except Exception as e:
            logger.error(f"Error al actualizar sugerencia {suggestion_id}: {str(e)}")
            return {"status": "error", "message": f"Error interno: {str(e)}"}
    
    def delete_suggestion(self, suggestion_id: int, user_id: int = None) -> Dict[str, Any]:
        """Elimina una sugerencia (solo el propietario o admin)."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                if user_id:
                    # Solo el propietario puede eliminar
                    cursor.execute("DELETE FROM suggestions WHERE id = ? AND user_id = ?", 
                                 (suggestion_id, user_id))
                else:
                    # Admin puede eliminar cualquier sugerencia
                    cursor.execute("DELETE FROM suggestions WHERE id = ?", (suggestion_id,))
                
                if cursor.rowcount == 0:
                    return {"status": "error", "message": "Sugerencia no encontrada o sin permisos"}
                
                conn.commit()
                
                logger.info(f"Sugerencia {suggestion_id} eliminada")
                
                return {"status": "success", "message": "Sugerencia eliminada exitosamente"}
                
        except Exception as e:
            logger.error(f"Error al eliminar sugerencia {suggestion_id}: {str(e)}")
            return {"status": "error", "message": f"Error interno: {str(e)}"}
    
    def get_suggestion_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de sugerencias."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Estadísticas generales
                cursor.execute("SELECT COUNT(*) as total FROM suggestions")
                total = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as pending FROM suggestions WHERE status = 'pending'")
                pending = cursor.fetchone()['pending']
                
                cursor.execute("SELECT COUNT(*) as approved FROM suggestions WHERE status = 'approved'")
                approved = cursor.fetchone()['approved']
                
                cursor.execute("SELECT COUNT(*) as rejected FROM suggestions WHERE status = 'rejected'")
                rejected = cursor.fetchone()['rejected']
                
                cursor.execute("SELECT COUNT(*) as in_progress FROM suggestions WHERE status = 'in_progress'")
                in_progress = cursor.fetchone()['in_progress']
                
                # Sugerencias recientes (últimos 7 días)
                week_ago = datetime.now() - timedelta(days=7)
                cursor.execute("SELECT COUNT(*) as recent FROM suggestions WHERE created_at >= ?", (week_ago,))
                recent = cursor.fetchone()['recent']
                
                # Top categorías
                cursor.execute('''
                    SELECT category, COUNT(*) as count 
                    FROM suggestions 
                    GROUP BY category 
                    ORDER BY count DESC 
                    LIMIT 5
                ''')
                top_categories = {row['category']: row['count'] for row in cursor.fetchall()}
                
                # Top prioridades
                cursor.execute('''
                    SELECT priority, COUNT(*) as count 
                    FROM suggestions 
                    GROUP BY priority 
                    ORDER BY count DESC 
                    LIMIT 5
                ''')
                top_priorities = {row['priority']: row['count'] for row in cursor.fetchall()}
                
                return {
                    "total_suggestions": total,
                    "pending_suggestions": pending,
                    "approved_suggestions": approved,
                    "rejected_suggestions": rejected,
                    "in_progress_suggestions": in_progress,
                    "recent_suggestions": recent,
                    "top_categories": top_categories,
                    "top_priorities": top_priorities
                }
                
        except Exception as e:
            logger.error(f"Error al obtener estadísticas: {str(e)}")
            return {
                "total_suggestions": 0,
                "pending_suggestions": 0,
                "approved_suggestions": 0,
                "rejected_suggestions": 0,
                "in_progress_suggestions": 0,
                "recent_suggestions": 0,
                "top_categories": {},
                "top_priorities": {}
            }
    
    def cleanup_old_suggestions(self, days_to_keep: int = 365) -> Dict[str, Any]:
        """Limpia sugerencias antiguas (más de X días)."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Contar sugerencias a eliminar
                cursor.execute("SELECT COUNT(*) as count FROM suggestions WHERE created_at < ?", (cutoff_date,))
                count_to_delete = cursor.fetchone()['count']
                
                # Eliminar sugerencias antiguas
                cursor.execute("DELETE FROM suggestions WHERE created_at < ?", (cutoff_date,))
                deleted_count = cursor.rowcount
                
                conn.commit()
                
                logger.info(f"Limpieza completada: {deleted_count} sugerencias eliminadas")
                
                return {
                    "status": "success",
                    "message": f"Limpieza completada",
                    "deleted_count": deleted_count,
                    "expected_count": count_to_delete
                }
                
        except Exception as e:
            logger.error(f"Error en limpieza: {str(e)}")
            return {"status": "error", "message": f"Error en limpieza: {str(e)}"}

# Instancia global del servicio
suggestions_service = SuggestionsService() 