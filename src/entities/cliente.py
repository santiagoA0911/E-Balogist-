from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Cliente:
    id_cliente: UUID = field(default_factory=uuid4)
    nombre: str = ""
    documento: str = ""
    telefono: str = ""
    correo: str = ""
    direccion: str = ""
