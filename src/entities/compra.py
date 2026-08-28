from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Compra:
    id_compra: UUID = field(default_factory=uuid4)
    fecha: date = field(default_factory=date.today)
    valor_total: float = 0
    estado: str = "Pendiente"
    id_proveedor: UUID | None = None
