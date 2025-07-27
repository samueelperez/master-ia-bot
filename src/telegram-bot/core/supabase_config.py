"""
Configuración de Supabase para Telegram Bot
Proporciona una interfaz unificada para interactuar con Supabase desde el bot
"""

import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import httpx

# Cargar .env desde el directorio raíz del proyecto
try:
    from dotenv import load_dotenv
    # Buscar el archivo .env en el directorio raíz del proyecto
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env')
    load_dotenv(env_path)
except ImportError:
    pass  # dotenv opcional en producción

logger = logging.getLogger(__name__)

class SupabaseConfig:
    """Configuración centralizada para Supabase."""
    
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.anon_key = os.getenv('SUPABASE_ANON_KEY')
        self.service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        if not self.url or not self.anon_key:
            logger.warning("SUPABASE_URL y SUPABASE_ANON_KEY no están configurados. Usando modo local.")
            self.enabled = False
            return
        
        self.enabled = True
        
        # Importar Supabase solo si está disponible
        try:
            from supabase import create_client, Client
            from supabase.lib.client_options import ClientOptions
            
            # Crear cliente con opciones optimizadas
            options = ClientOptions(
                schema='public',
                headers={
                    'X-Client-Info': 'crypto-ai-bot-telegram/1.0.0'
                }
            )
            
            self.client: Client = create_client(
                supabase_url=self.url,
                supabase_key=self.anon_key,
                options=options
            )
            
            # Cliente con service role para operaciones administrativas
            if self.service_role_key:
                self.admin_client: Client = create_client(
                    supabase_url=self.url,
                    supabase_key=self.service_role_key,
                    options=options
                )
            else:
                self.admin_client = self.client
                
            logger.info("✅ Supabase configurado correctamente para Telegram Bot")
            
        except ImportError:
            logger.warning("Supabase no está instalado. Usando modo local.")
            self.enabled = False
        except Exception as e:
            logger.error(f"❌ Error configurando Supabase: {e}")
            self.enabled = False
    
    def test_connection(self) -> bool:
        """Prueba la conexión con Supabase."""
        if not self.enabled:
            return False
            
        try:
            # Intentar una consulta simple
            result = self.client.table('telegram_users').select('id').limit(1).execute()
            logger.info("✅ Conexión a Supabase exitosa")
            return True
        except Exception as e:
            logger.error(f"❌ Error conectando a Supabase: {e}")
            return False

class SupabaseService:
    """Servicio para operaciones comunes con Supabase desde el bot."""
    
    def __init__(self):
        self.config = SupabaseConfig()
        if self.config.enabled:
            self.client = self.config.client
            self.admin_client = self.config.admin_client
        else:
            self.client = None
            self.admin_client = None
    
    # ========================================
    # OPERACIONES DE USUARIOS
    # ========================================
    
    def create_or_update_user(self, telegram_id: int, username: str = None, 
                             first_name: str = None, last_name: str = None) -> bool:
        """Crea o actualiza un usuario de Telegram en Supabase."""
        if not self.config.enabled:
            logger.debug("Supabase no está habilitado, saltando creación de usuario")
            return True
            
        try:
            user_data = {
                'telegram_id': telegram_id,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'last_activity': datetime.now(timezone.utc).isoformat()
            }
            
            # Intentar insertar, si existe actualizar
            result = self.client.table('telegram_users').upsert(
                user_data, 
                on_conflict='telegram_id'
            ).execute()
            
            if result.data:
                logger.info(f"✅ Usuario {telegram_id} creado/actualizado en Supabase")
                return True
            else:
                logger.error("No se pudo crear/actualizar el usuario en Supabase")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error creando/actualizando usuario {telegram_id} en Supabase: {e}")
            return False
    
    def get_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un usuario por su telegram_id desde Supabase."""
        if not self.config.enabled:
            return None
            
        try:
            result = self.client.table('telegram_users').select('*').eq(
                'telegram_id', telegram_id
            ).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo usuario {telegram_id} de Supabase: {e}")
            return None
    
    def update_user_activity(self, telegram_id: int) -> bool:
        """Actualiza la última actividad de un usuario en Supabase."""
        if not self.config.enabled:
            return True
            
        try:
            self.client.table('telegram_users').update({
                'last_activity': datetime.now(timezone.utc).isoformat()
            }).eq('telegram_id', telegram_id).execute()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error actualizando actividad de usuario {telegram_id} en Supabase: {e}")
            return False
    
    # ========================================
    # OPERACIONES DE SUGERENCIAS
    # ========================================
    
    def create_suggestion(self, user_id: int, suggestion_text: str, 
                         user_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Crea una nueva sugerencia en Supabase."""
        if not self.config.enabled:
            logger.debug("Supabase no está habilitado, saltando creación de sugerencia")
            return {"status": "error", "message": "Supabase no está configurado"}
            
        try:
            suggestion_data = {
                'user_id': user_id,
                'suggestion_text': suggestion_text,
                'user_info': user_info or {},
                'status': 'pending'
            }
            
            result = self.client.table('suggestions').insert(suggestion_data).execute()
            
            if result.data:
                logger.info(f"✅ Sugerencia creada en Supabase para usuario {user_id}")
                return {
                    "status": "success",
                    "id": result.data[0]['id'],
                    "message": "Sugerencia creada exitosamente"
                }
            else:
                return {"status": "error", "message": "No se pudo crear la sugerencia"}
                
        except Exception as e:
            logger.error(f"❌ Error creando sugerencia para usuario {user_id} en Supabase: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_suggestions(self, limit: int = 50, status: str = None) -> List[Dict[str, Any]]:
        """Obtiene sugerencias con filtros opcionales desde Supabase."""
        if not self.config.enabled:
            return []
            
        try:
            query = self.client.table('suggestions').select('*').order('created_at', desc=True)
            
            if status:
                query = query.eq('status', status)
            
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo sugerencias de Supabase: {e}")
            return []
    
    # ========================================
    # OPERACIONES DE ALERTAS
    # ========================================
    
    def create_alert(self, user_id: int, symbol: str, condition_type: str,
                    condition_value: float, timeframe: str) -> Dict[str, Any]:
        """Crea una nueva alerta en Supabase."""
        if not self.config.enabled:
            logger.debug("Supabase no está habilitado, saltando creación de alerta")
            return {"status": "error", "message": "Supabase no está configurado"}
            
        try:
            alert_data = {
                'user_id': user_id,
                'symbol': symbol,
                'condition_type': condition_type,
                'condition_value': condition_value,
                'timeframe': timeframe,
                'is_active': True
            }
            
            result = self.client.table('alerts').insert(alert_data).execute()
            
            if result.data:
                logger.info(f"✅ Alerta creada en Supabase para usuario {user_id}")
                return {
                    "status": "success",
                    "id": result.data[0]['id'],
                    "message": "Alerta creada exitosamente"
                }
            else:
                return {"status": "error", "message": "No se pudo crear la alerta"}
                
        except Exception as e:
            logger.error(f"❌ Error creando alerta para usuario {user_id} en Supabase: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_user_alerts(self, user_id: int, active_only: bool = True) -> List[Dict[str, Any]]:
        """Obtiene las alertas de un usuario desde Supabase."""
        if not self.config.enabled:
            return []
            
        try:
            query = self.client.table('alerts').select('*').eq('user_id', user_id)
            
            if active_only:
                query = query.eq('is_active', True)
            
            result = query.order('created_at', desc=True).execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo alertas del usuario {user_id} de Supabase: {e}")
            return []
    
    def delete_alert(self, alert_id: str, user_id: int) -> bool:
        """Elimina una alerta desde Supabase."""
        if not self.config.enabled:
            return True
            
        try:
            self.client.table('alerts').delete().eq('id', alert_id).eq('user_id', user_id).execute()
            
            logger.info(f"✅ Alerta {alert_id} eliminada de Supabase")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error eliminando alerta {alert_id} de Supabase: {e}")
            return False
    
    # ========================================
    # OPERACIONES DE LOGS
    # ========================================
    
    def log_activity(self, user_id: int, action: str, details: Dict[str, Any] = None,
                    ip_address: str = None, user_agent: str = None) -> bool:
        """Registra una actividad del usuario en Supabase."""
        if not self.config.enabled:
            return True
            
        try:
            log_data = {
                'user_id': user_id,
                'action': action,
                'details': details or {},
                'ip_address': ip_address,
                'user_agent': user_agent
            }
            
            self.client.table('activity_logs').insert(log_data).execute()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error registrando actividad del usuario {user_id} en Supabase: {e}")
            return False
    
    # ========================================
    # OPERACIONES DE CONFIGURACIÓN
    # ========================================
    
    def get_user_configuration(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene la configuración de un usuario desde Supabase."""
        if not self.config.enabled:
            return None
            
        try:
            result = self.client.table('user_configurations').select('*').eq('user_id', user_id).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo configuración del usuario {user_id} de Supabase: {e}")
            return None
    
    def update_user_configuration(self, user_id: int, config_data: Dict[str, Any]) -> bool:
        """Actualiza la configuración de un usuario en Supabase."""
        if not self.config.enabled:
            return True
            
        try:
            config_data['user_id'] = user_id
            
            self.client.table('user_configurations').upsert(
                config_data, 
                on_conflict='user_id'
            ).execute()
            
            logger.info(f"✅ Configuración actualizada en Supabase para usuario {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error actualizando configuración del usuario {user_id} en Supabase: {e}")
            return False

# Instancia global del servicio
supabase_service = SupabaseService() 