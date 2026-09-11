from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.connection import AuditModel


class Cliente(AuditModel):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    documento = Column(String(30), nullable=False, unique=True)
    telefono = Column(String(30), nullable=False)
    correo = Column(String(120), nullable=False)
    direccion = Column(String(150), nullable=False)

    pedidos = relationship("Pedido", back_populates="cliente")

    def __repr__(self):
        return f"Cliente(ID: {self.id}, Nombre: {self.nombre}, Documento: {self.documento})"
