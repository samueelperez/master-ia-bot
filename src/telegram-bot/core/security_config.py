import os
from typing import List, Dict, Any
from dataclasses import dataclass
import hashlib
import time

@dataclass
class TelegramSecurityConfig:
    """Configuración de seguridad para el bot de Telegram."""
    

    
    # Timeouts (en segundos)
    AI_MODULE_TIMEOUT: int = int(os.getenv("AI_MODULE_TIMEOUT", "60"))
    HEALTH_CHECK_TIMEOUT: int = int(os.getenv("HEALTH_CHECK_TIMEOUT", "5"))
    MAX_MESSAGE_LENGTH: int = int(os.getenv("MAX_MESSAGE_LENGTH", "4000"))
    
    # Autenticación de usuarios - se cargan dinámicamente para evitar mutabilidad
    
    # Configuración de memoria/base de datos
    MAX_CONVERSATION_HISTORY: int = int(os.getenv("MAX_CONVERSATION_HISTORY", "100"))
    MAX_ALERTS_PER_USER: int = int(os.getenv("MAX_ALERTS_PER_USER", "50"))
    DB_CONNECTION_TIMEOUT: int = int(os.getenv("DB_CONNECTION_TIMEOUT", "30"))
    
    # Patrones de seguridad
    DANGEROUS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"vbscript:",
        r"onload\s*=",
        r"onerror\s*=",
        r"eval\s*\(",
        r"setTimeout\s*\(",
        r"setInterval\s*\(",
        r"\b(union|select|insert|update|delete|drop)\b.*\b(from|into|set|table)\b",
        r"['\";].*(\-\-|\/\*|\*\/)",
        r"(system|exec|shell_exec|passthru)\s*\(",
        r"(file_get_contents|file_put_contents|fopen|fwrite)\s*\("
    ]
    
    # Lista blanca de símbolos permitidos
    ALLOWED_SYMBOLS = [
        "BTC", "ETH", "SOL", "XRP", "ADA", "DOGE", "SHIB", "BNB", "DOT", "AVAX",
        "MATIC", "ATOM", "LINK", "UNI", "AAVE", "SUSHI", "CRV", "COMP", "YFI", "SNX",
        "1INCH", "BAL", "LRC", "ZRX", "ALPHA", "BADGER", "BAND", "CREAM", "DFI", "FARM",
        "HEGIC", "KNC", "PICKLE", "REN", "RUNE", "SAND"
    ]
    
    # Timeframes válidos
    ALLOWED_TIMEFRAMES = ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]
    
    @classmethod
    def is_user_authorized(cls, user_id: int) -> bool:
        """Verifica si un usuario está autorizado."""
        users_str = os.getenv("AUTHORIZED_TELEGRAM_USERS", "")
        if not users_str.strip():  # Si está vacío, permite todos (desarrollo)
            return True
        authorized_users = [
            int(x.strip()) for x in users_str.split(",") 
            if x.strip().isdigit()
        ]
        return user_id in authorized_users
    
    @classmethod
    def is_admin_user(cls, user_id: int) -> bool:
        """Verifica si un usuario es admin."""
        users_str = os.getenv("TELEGRAM_ADMIN_USERS", "")
        if not users_str.strip():
            return False
        admin_users = [
            int(x.strip()) for x in users_str.split(",") 
            if x.strip().isdigit()
        ]
        return user_id in admin_users
    
    @classmethod
    def validate_symbol(cls, symbol: str) -> bool:
        """Valida que el símbolo esté en la lista permitida."""
        return symbol.upper() in cls.ALLOWED_SYMBOLS
    
    @classmethod
    def validate_timeframe(cls, timeframe: str) -> bool:
        """Valida que el timeframe esté permitido."""
        return timeframe in cls.ALLOWED_TIMEFRAMES



class TelegramInputValidator:
    """Validador de entrada para el bot de Telegram."""
    
    @staticmethod
    def sanitize_message(message: str) -> str:
        """Sanitiza un mensaje de entrada."""
        if not message:
            return ""
        
        # Truncar mensaje si es muy largo
        if len(message) > TelegramSecurityConfig.MAX_MESSAGE_LENGTH:
            message = message[:TelegramSecurityConfig.MAX_MESSAGE_LENGTH]
        
        # Remover caracteres peligrosos
        import re
        for pattern in TelegramSecurityConfig.DANGEROUS_PATTERNS:
            message = re.sub(pattern, "", message, flags=re.IGNORECASE)
        
        return message.strip()
    
    @staticmethod
    def validate_user_input(text: str, input_type: str = "message") -> tuple[bool, str]:
        """
        Valida entrada del usuario.
        
        Args:
            text: Texto a validar
            input_type: Tipo de entrada (message, symbol, timeframe, value)
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not text:
            return False, "Entrada vacía no permitida"
        
        import re
        
        # Verificar patrones peligrosos
        for pattern in TelegramSecurityConfig.DANGEROUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return False, f"Patrón peligroso detectado en entrada de tipo {input_type}"
        
        # Validaciones específicas por tipo
        if input_type == "symbol":
            symbol = text.upper().strip()
            if not TelegramSecurityConfig.validate_symbol(symbol):
                return False, f"Símbolo '{symbol}' no está en la lista permitida"
        
        elif input_type == "timeframe":
            timeframe = text.lower().strip()
            if not TelegramSecurityConfig.validate_timeframe(timeframe):
                return False, f"Timeframe '{timeframe}' no es válido"
        
        elif input_type == "value":
            try:
                value = float(text)
                if value <= 0 or value > 1000000:  # Límites razonables
                    return False, "Valor debe estar entre 0 y 1,000,000"
            except ValueError:
                return False, "Valor debe ser un número válido"
        
        return True, ""

class TelegramSecureLogger:
    """Logger seguro para el bot de Telegram."""
    
    def __init__(self):
        import logging
        import os
        
        # Crear directorio de logs si no existe
        log_dir = os.getenv("TELEGRAM_LOG_DIR", "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        # Configurar logger
        self.logger = logging.getLogger("telegram_bot")
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            # Handler para archivo
            file_handler = logging.FileHandler(f"{log_dir}/telegram_bot.log")
            file_handler.setLevel(logging.INFO)
            
            # Handler para consola
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)
            
            # Formato
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def safe_log(self, message: str, level: str = "info", user_id: int = None):
        """Log seguro que no expone información sensible."""
        # Enmascarar user_id para privacidad
        if user_id:
            masked_user = f"user_{hashlib.sha256(str(user_id).encode()).hexdigest()[:8]}"
            message = f"[{masked_user}] {message}"
        
        # Remover posibles tokens o claves
        import re
        message = re.sub(r'\b\d{10,15}:\w{30,50}\b', '[TELEGRAM_TOKEN]', message)
        message = re.sub(r'\bsk-\w{40,60}\b', '[API_KEY]', message)
        
        if level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "debug":
            self.logger.debug(message) 