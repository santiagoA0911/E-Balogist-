from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Producto:
    id_producto: UUID = field(default_factory=uuid4)
    nombre: str = ""
    descripcion: str = ""
    categoria: str = ""
    precio: float = 0
