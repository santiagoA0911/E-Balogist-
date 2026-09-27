from pydantic import BaseModel


class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str
    categoria: str
    precio: float


class ProductoUpdate(BaseModel):
    nombre: str
    descripcion: str
    categoria: str
    precio: float


class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    categoria: str
    precio: float