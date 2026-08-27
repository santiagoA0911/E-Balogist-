from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Material:
    id_material: UUID = field(default_factory=uuid4)
    nombre: str = ""
    tipo: str = ""
    cantidad: float = 0
    unidad: str = ""
    precio: float = 0
