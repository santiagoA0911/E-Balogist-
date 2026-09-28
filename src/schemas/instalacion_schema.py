from pydantic import BaseModel
from typing import Optional
from datetime import date

class InstalacionBase(BaseModel):
    ubicacion: str
    fecha_instalacion: date
    id_transporte: int  # Llave foránea hacia Transporte

class InstalacionCreate(InstalacionBase):
    pass

class InstalacionUpdate(BaseModel):
    ubicacion: Optional[str] = None
    fecha_instalacion: Optional[date] = None
    id_transporte: Optional[int] = None

class InstalacionResponse(InstalacionBase):
    id_instalacion: int

    class Config:
        from_attributes = True