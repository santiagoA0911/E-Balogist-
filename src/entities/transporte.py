from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.connection import AuditModel

class Transporte(AuditModel):
    __tablename__ = "transportes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    origen = Column(String(100), nullable=False)
    destino = Column(String(100), nullable=False)
    estado = Column(String(50), default="En espera")
    produccion_id = Column(Integer, ForeignKey("producciones.id"), nullable=True)

    produccion = relationship("Produccion")

    def __repr__(self):
        return f"Transporte(ID: {self.id}, Origen: {self.origen}, Destino: {self.destino})"