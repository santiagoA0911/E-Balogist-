from decimal import Decimal

from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship
from src.database.connection import AuditModel


class DetallePedido(AuditModel):
    """Linea de un pedido. precio_unitario se congela al agregar el item."""

    __tablename__ = "detalles_pedido"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Numeric(10, 2), nullable=False, default=1)
    precio_unitario = Column(Numeric(12, 2), nullable=False, default=0)

    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")

    @property
    def subtotal(self) -> Decimal:
        """No se guarda: se deduce de cantidad y precio_unitario."""
        return Decimal(self.cantidad or 0) * Decimal(self.precio_unitario or 0)

    def __repr__(self):
        return f"DetallePedido(ID: {self.id}, Pedido: {self.pedido_id}, Subtotal: {self.subtotal})"
