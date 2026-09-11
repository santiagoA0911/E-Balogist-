from sqlalchemy import Column, Integer, String
from src.database.connection import AuditModel

class Empleado(AuditModel):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=False)
    estado = Column(String(50), default="Activo")

    def __repr__(self):
        return f"Empleado(ID: {self.id}, Nombre: {self.nombre}, Cargo: {self.cargo}, Estado: {self.estado})"