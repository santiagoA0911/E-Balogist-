from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class DetallePedido:
    id_detalle: UUID = field(default_factory=uuid4)
    id_pedido: UUID | None = None
    id_producto: UUID | None = None
    cantidad: float = 0
    precio_unitario: float = 0

    @property
    def subtotal(self) -> float:
        return self.cantidad * self.precio_unitario
