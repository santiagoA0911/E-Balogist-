from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Proveedor:
    id_proveedor: UUID = field(default_factory=uuid4)
    nombre: str = ""
    tel: str = ""
    direccion: str = ""
    correo: str = ""
