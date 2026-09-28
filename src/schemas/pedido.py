from pydantic import BaseModel


class PedidoCreate(BaseModel):
    cliente_id: int
    fecha: str
    fecha_entrega: str | None = None
    estado: str
    direccion_entrega: str


class PedidoUpdate(BaseModel):
    cliente_id: int
    fecha: str
    fecha_entrega: str | None = None
    estado: str
    direccion_entrega: str


class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    fecha: str
    fecha_entrega: str
    estado: str
    direccion_entrega: str
    valor_total: float