#!/bin/bash
set -e

# Crear directorios necesarios
mkdir -p /app/logs /app/pids

# Lanzar solo el backend
cd src/backend && uvicorn main_secure:app --host 0.0.0.0 --port 8000 