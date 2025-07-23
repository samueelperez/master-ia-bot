# Dockerfile simple y directo para Railway
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración
COPY requirements/ ./requirements/
COPY railway.toml ./

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements/common.txt

# Copiar código fuente
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY docs/ ./docs/
COPY config/ ./config/

# Instalar dependencias de Node.js para webapp
WORKDIR /app/src/webapp
RUN npm ci --only=production
WORKDIR /app

# Crear directorios necesarios
RUN mkdir -p /app/logs /app/pids

# Copiar el nuevo script de inicio y Procfile
COPY start.sh /app/start.sh
COPY Procfile /app/Procfile
RUN chmod +x /app/start.sh

# Exponer puertos
EXPOSE 3000 8000 9004 9005

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/railway-health || exit 1

# Comando por defecto
CMD ["/app/start.sh"] 