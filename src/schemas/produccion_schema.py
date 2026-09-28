from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProduccionBase(BaseModel):
    cantidad: int
    fecha: date
    id_empleado: int  # Llave foránea hacia Empleado

class ProduccionCreate(ProduccionBase):
    pass

class ProduccionUpdate(BaseModel):
    cantidad: Optional[int] = None
    fecha: Optional[date] = None
    id_empleado: Optional[int] = None

class ProduccionResponse(ProduccionBase):
    id_produccion: int

    class Config:
        from_attributes = True