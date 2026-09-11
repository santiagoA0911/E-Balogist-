import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("La variable DATABASE_URL no está configurada en el archivo .env")

# Crear el motor de conexión a Neon PostgreSQL
engine = create_engine(DATABASE_URL)

# Generador de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa de SQLAlchemy
Base = declarative_base()

# Modelo base con los 4 campos de auditoría requeridos por el profesor
class AuditModel(Base):
    __abstract__ = True

    id_usuario_creacion = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True)
    id_usuario_edicion = Column(UUID(as_uuid=True), default=uuid.uuid4, onupdate=uuid.uuid4, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_edicion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()