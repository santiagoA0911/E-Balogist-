from pydantic import BaseModel
from typing import Optional

class TransporteBase(BaseModel):
    vehiculo: str
    destino: str
    id_produccion: int  # Llave foránea hacia Producción

class TransporteCreate(TransporteBase):
    pass

class TransporteUpdate(BaseModel):
    vehiculo: Optional[str] = None
    destino: Optional[str] = None
    id_produccion: Optional[int] = None

class TransporteResponse(TransporteBase):
    id_transporte: int

    class Config:
        from_attributes = True