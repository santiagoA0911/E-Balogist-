from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Pedido:
    id_pedido: UUID = field(default_factory=uuid4)
    id_cliente: UUID | None = None
    fecha: date = field(default_factory=date.today)
    fecha_entrega: date = field(default_factory=date.today)
    estado: str = "Pendiente"
    direccion_entrega: str = ""
    valor_total: float = 0
