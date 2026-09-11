from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.connection import AuditModel

class Instalacion(AuditModel):
    __tablename__ = "instalaciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    direccion = Column(String(150), nullable=False)
    estado = Column(String(50), default="Programada")
    transporte_id = Column(Integer, ForeignKey("transportes.id"), nullable=True)

    transporte = relationship("Transporte")

    def __repr__(self):
        return f"Instalacion(ID: {self.id}, Direccion: {self.direccion}, Estado: {self.estado})"