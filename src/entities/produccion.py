from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.connection import AuditModel

class Produccion(AuditModel):
    __tablename__ = "producciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    trabajo = Column(String(150), nullable=False)
    estado = Column(String(50), default="Pendiente")
    empleado_id = Column(Integer, ForeignKey("empleados.id"), nullable=True)

    empleado = relationship("Empleado")

    def __repr__(self):
        return f"Produccion(ID: {self.id}, Trabajo: {self.trabajo}, Estado: {self.estado})"