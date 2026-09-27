from pydantic import BaseModel


class DetallePedidoCreate(BaseModel):
    pedido_id: int
    producto_id: int
    cantidad: float


class DetallePedidoUpdate(BaseModel):
    cantidad: float


class DetallePedidoResponse(BaseModel):
    id: int
    pedido_id: int
    producto_id: int
    cantidad: float
    precio_unitario: float
    subtotal: float