from datetime import date
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MaterialCreate(BaseModel):
    nombre: str
    tipo: str
    cantidad: float
    unidad: str
    precio: float


class MaterialUpdate(BaseModel):
    nombre: str | None = None
    tipo: str | None = None
    cantidad: float | None = None
    unidad: str | None = None
    precio: float | None = None


class MaterialRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_material: UUID
    nombre: str
    tipo: str
    cantidad: float
    unidad: str
    precio: float


class materialPost(BaseModel):
    data: MaterialRead
    status: int
    message: str


class MaterialList(BaseModel):
    data: List[MaterialRead]
    status: int
    message: str


class materialPut(BaseModel):
    data: MaterialRead
    status: int
    message: str


class CompraCreate(BaseModel):
    fecha: date
    valor_total: float
    estado: str = "Pendiente"
    id_proveedor: UUID | None = None


class CompraUpdate(BaseModel):
    fecha: date | None = None
    valor_total: float | None = None
    estado: str | None = None
    id_proveedor: UUID | None = None


class CompraRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_compra: UUID
    fecha: date
    valor_total: float
    estado: str
    id_proveedor: UUID | None = None


class compraPost(BaseModel):
    data: CompraRead
    status: int
    message: str


class CompraList(BaseModel):
    data: List[CompraRead]
    status: int
    message: str


class compraPut(BaseModel):
    data: CompraRead
    status: int
    message: str


class ProveedorCreate(BaseModel):
    nombre: str
    tel: str
    direccion: str
    correo: str


class ProveedorUpdate(BaseModel):
    nombre: str | None = None
    tel: str | None = None
    direccion: str | None = None
    correo: str | None = None


class ProveedorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_proveedor: UUID
    nombre: str
    tel: str
    direccion: str
    correo: str


class proveedorPost(BaseModel):
    data: ProveedorRead
    status: int
    message: str


class ProveedorList(BaseModel):
    data: List[ProveedorRead]
    status: int
    message: str


class proveedorPut(BaseModel):
    data: ProveedorRead
    status: int
    message: str
