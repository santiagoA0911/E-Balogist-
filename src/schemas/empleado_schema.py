from pydantic import BaseModel
from typing import Optional

# 1. Esquema Base: Campos comunes que comparte la entidad
class EmpleadoBase(BaseModel):
    nombre: str
    cargo: str
    estado: str

# 2. Esquema para CREAR (POST): Hereda de Base
class EmpleadoCreate(EmpleadoBase):
    pass

# 3. Esquema para ACTUALIZAR (PUT): Todos los campos opcionales para modificaciones parciales
class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    cargo: Optional[str] = None
    estado: Optional[str] = None

# 4. Esquema de RESPUESTA (GET): Incluye la llave primaria e integra con SQLAlchemy
class EmpleadoResponse(EmpleadoBase):
    id_empleado: int

    class Config:
        from_attributes = True  # Mapea los atributos de SQLAlchemy a Pydantic