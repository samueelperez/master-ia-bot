from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Cadena de conexión a Postgres desde variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://botuser:botpass@127.0.0.1:5432/botdb")

# Si estamos en Render y la URL no tiene el formato correcto, ajustarla
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,  # Reciclar conexiones cada 5 minutos
    pool_size=10,      # Tamaño del pool de conexiones
    max_overflow=20    # Conexiones adicionales permitidas
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
