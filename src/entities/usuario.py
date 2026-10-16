
from sqlalchemy import Column, Integer, String, Boolean
from src.database.connection import AuditModel


class Usuario(AuditModel):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(120), nullable=False, unique=True)
    activo = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"Usuario(ID: {self.id}, Nombre: {self.nombre}, Correo: {self.correo})"
