from pydantic import BaseModel


class ClienteCreate(BaseModel):
    nombre: str
    documento: str
    telefono: str
    correo: str
    direccion: str


class ClienteUpdate(BaseModel):
    nombre: str
    documento: str
    telefono: str
    correo: str
    direccion: str


class ClienteResponse(BaseModel):
    id: int
    nombre: str
    documento: str
    telefono: str
    correo: str
    direccion: str