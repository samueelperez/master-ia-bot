#!/usr/bin/env python3
"""
Script temporal para corregir el manejo de strategy_type en advanced_strategies_service.py
"""

import re

# Leer el archivo
with open('core/services/advanced_strategies_service.py', 'r') as f:
    content = f.read()

# Reemplazar todas las ocurrencias de strategy_type.value
content = re.sub(
    r'strategy_type\.value',
    'strategy_type.value if hasattr(strategy_type, "value") else str(strategy_type)',
    content
)

# Escribir el archivo corregido
with open('core/services/advanced_strategies_service.py', 'w') as f:
    f.write(content)

print("✅ Archivo corregido exitosamente") 