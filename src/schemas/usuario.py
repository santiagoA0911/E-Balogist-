
from pydantic import BaseModel, ConfigDict


class UsuarioCreate(BaseModel):
    nombre: str
    correo: str
    activo: bool = True


class UsuarioUpdate(BaseModel):
    nombre: str
    correo: str
    activo: bool


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    correo: str
    activo: bool

    model_config = ConfigDict(from_attributes=True)
