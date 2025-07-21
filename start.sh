#!/bin/bash
set -e

# Instalar honcho si no está instalado
pip install --no-cache-dir honcho

# Crear directorios necesarios
mkdir -p /app/logs /app/pids

# Lanzar todos los servicios con honcho
honcho start 