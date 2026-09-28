from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.orm import relationship
from src.database.connection import AuditModel


class Producto(AuditModel):
    """Producto terminado que se vende. No lleva stock: se fabrica bajo pedido."""

    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=False, default="")
    categoria = Column(String(50), nullable=False)
    precio = Column(Numeric(12, 2), nullable=False, default=0)

    detalles = relationship("DetallePedido", back_populates="producto")

    def __repr__(self):
        return f"Producto(ID: {self.id}, Nombre: {self.nombre}, Precio: {self.precio})"
