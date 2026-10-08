from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from src.database.connection import AuditModel


class Pedido(AuditModel):
    """Encargo de un cliente. El valor_total no se digita: lo recalcula PedidoCRUD."""

    __tablename__ = "pedidos"

    ESTADOS = ("Pendiente", "En produccion", "En transito", "Instalado", "Cancelado")

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    fecha = Column(Date, nullable=False, default=date.today)
    fecha_entrega = Column(Date, nullable=True)
    estado = Column(String(30), nullable=False, default="Pendiente")
    direccion_entrega = Column(String(150), nullable=False)
    valor_total = Column(Numeric(12, 2), nullable=False, default=0)

    cliente = relationship("Cliente", back_populates="pedidos")
    detalles = relationship(
        "DetallePedido",
        back_populates="pedido",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"Pedido(ID: {self.id}, Estado: {self.estado}, Total: {self.valor_total})"
