"""
Configuración de Supabase para Crypto AI Bot
Proporciona una interfaz unificada para interactuar con Supabase
"""

import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import httpx
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

logger = logging.getLogger(__name__)

class SupabaseConfig:
    """Configuración centralizada para Supabase."""
    
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.anon_key = os.getenv('SUPABASE_ANON_KEY')
        self.service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        if not self.url or not self.anon_key:
            raise ValueError("SUPABASE_URL y SUPABASE_ANON_KEY deben estar configurados")
        
        # Crear cliente con opciones optimizadas
        options = ClientOptions(
            schema='public',
            headers={
                'X-Client-Info': 'crypto-ai-bot/1.0.0'
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
            
        logger.info("✅ Supabase configurado correctamente")
    
    def test_connection(self) -> bool:
        """Prueba la conexión con Supabase."""
        try:
            # Intentar una consulta simple
            result = self.client.table('telegram_users').select('id').limit(1).execute()
            logger.info("✅ Conexión a Supabase exitosa")
            return True
        except Exception as e:
            logger.error(f"❌ Error conectando a Supabase: {e}")
            return False

class SupabaseService:
    """Servicio para operaciones comunes con Supabase."""
    
    def __init__(self):
        self.config = SupabaseConfig()
        self.client = self.config.client
        self.admin_client = self.config.admin_client
    
    # ========================================
    # OPERACIONES DE USUARIOS
    # ========================================
    
    def create_or_update_user(self, telegram_id: int, username: str = None, 
                             first_name: str = None, last_name: str = None) -> Dict[str, Any]:
        """Crea o actualiza un usuario de Telegram."""
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
                logger.info(f"✅ Usuario {telegram_id} creado/actualizado")
                return result.data[0]
            else:
                raise Exception("No se pudo crear/actualizar el usuario")
                
        except Exception as e:
            logger.error(f"❌ Error creando/actualizando usuario {telegram_id}: {e}")
            raise
    
    def get_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un usuario por su telegram_id."""
        try:
            result = self.client.table('telegram_users').select('*').eq(
                'telegram_id', telegram_id
            ).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo usuario {telegram_id}: {e}")
            return None
    
    def update_user_activity(self, telegram_id: int) -> bool:
        """Actualiza la última actividad de un usuario."""
        try:
            self.client.table('telegram_users').update({
                'last_activity': datetime.now(timezone.utc).isoformat()
            }).eq('telegram_id', telegram_id).execute()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error actualizando actividad de usuario {telegram_id}: {e}")
            return False
    
    # ========================================
    # OPERACIONES DE SUGERENCIAS
    # ========================================
    
    def create_suggestion(self, user_id: int, suggestion_text: str, 
                         user_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Crea una nueva sugerencia."""
        try:
            suggestion_data = {
                'user_id': user_id,
                'suggestion_text': suggestion_text,
                'user_info': user_info or {},
                'status': 'pending'
            }
            
            result = self.client.table('suggestions').insert(suggestion_data).execute()
            
            if result.data:
                logger.info(f"✅ Sugerencia creada para usuario {user_id}")
                return result.data[0]
            else:
                raise Exception("No se pudo crear la sugerencia")
                
        except Exception as e:
            logger.error(f"❌ Error creando sugerencia para usuario {user_id}: {e}")
            raise
    
    def get_suggestions(self, limit: int = 50, status: str = None) -> List[Dict[str, Any]]:
        """Obtiene sugerencias con filtros opcionales."""
        try:
            query = self.client.table('suggestions').select('*').order('created_at', desc=True)
            
            if status:
                query = query.eq('status', status)
            
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo sugerencias: {e}")
            return []
    
    def update_suggestion_status(self, suggestion_id: str, status: str, 
                                admin_notes: str = None) -> bool:
        """Actualiza el estado de una sugerencia."""
        try:
            update_data = {'status': status}
            if admin_notes:
                update_data['admin_notes'] = admin_notes
            
            self.client.table('suggestions').update(update_data).eq('id', suggestion_id).execute()
            
            logger.info(f"✅ Sugerencia {suggestion_id} actualizada a {status}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error actualizando sugerencia {suggestion_id}: {e}")
            return False
    
    # ========================================
    # OPERACIONES DE ALERTAS
    # ========================================
    
    def create_alert(self, user_id: int, symbol: str, condition_type: str,
                    condition_value: float, timeframe: str) -> Dict[str, Any]:
        """Crea una nueva alerta."""
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
                logger.info(f"✅ Alerta creada para usuario {user_id}")
                return result.data[0]
            else:
                raise Exception("No se pudo crear la alerta")
                
        except Exception as e:
            logger.error(f"❌ Error creando alerta para usuario {user_id}: {e}")
            raise
    
    def get_user_alerts(self, user_id: int, active_only: bool = True) -> List[Dict[str, Any]]:
        """Obtiene las alertas de un usuario."""
        try:
            query = self.client.table('alerts').select('*').eq('user_id', user_id)
            
            if active_only:
                query = query.eq('is_active', True)
            
            result = query.order('created_at', desc=True).execute()
            
            return result.data or []
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo alertas del usuario {user_id}: {e}")
            return []
    
    def delete_alert(self, alert_id: str, user_id: int) -> bool:
        """Elimina una alerta."""
        try:
            self.client.table('alerts').delete().eq('id', alert_id).eq('user_id', user_id).execute()
            
            logger.info(f"✅ Alerta {alert_id} eliminada")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error eliminando alerta {alert_id}: {e}")
            return False
    
    # ========================================
    # OPERACIONES DE CONFIGURACIÓN
    # ========================================
    
    def get_user_configuration(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene la configuración de un usuario."""
        try:
            result = self.client.table('user_configurations').select('*').eq('user_id', user_id).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo configuración del usuario {user_id}: {e}")
            return None
    
    def update_user_configuration(self, user_id: int, config_data: Dict[str, Any]) -> bool:
        """Actualiza la configuración de un usuario."""
        try:
            config_data['user_id'] = user_id
            
            self.client.table('user_configurations').upsert(
                config_data, 
                on_conflict='user_id'
            ).execute()
            
            logger.info(f"✅ Configuración actualizada para usuario {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error actualizando configuración del usuario {user_id}: {e}")
            return False
    
    # ========================================
    # OPERACIONES DE LOGS
    # ========================================
    
    def log_activity(self, user_id: int, action: str, details: Dict[str, Any] = None,
                    ip_address: str = None, user_agent: str = None) -> bool:
        """Registra una actividad del usuario."""
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
            logger.error(f"❌ Error registrando actividad del usuario {user_id}: {e}")
            return False
    
    # ========================================
    # OPERACIONES ADMINISTRATIVAS
    # ========================================
    
    def get_suggestions_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de sugerencias."""
        try:
            result = self.admin_client.rpc('get_suggestions_stats').execute()
            return result.data or {}
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas de sugerencias: {e}")
            return {}
    
    def get_active_users_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de usuarios activos."""
        try:
            result = self.admin_client.rpc('get_active_users_stats').execute()
            return result.data or {}
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas de usuarios: {e}")
            return {}

# Instancia global del servicio
supabase_service = SupabaseService() 