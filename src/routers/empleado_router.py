from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database.connection import get_db
from src.entities.empleado import Empleado
from src.schemas.empleado_schema import EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse

router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.get("/", response_model=List[EmpleadoResponse], status_code=status.HTTP_200_OK)
def listar_empleados(db: Session = Depends(get_db)):
    return db.query(Empleado).all()

@router.get("/{id_empleado}", response_model=EmpleadoResponse, status_code=status.HTTP_200_OK)
def obtener_empleado(id_empleado: int, db: Session = Depends(get_db)):
    empleado = db.query(Empleado).filter(Empleado.id_empleado == id_empleado).first()
    if not empleado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado")
    return empleado

@router.post("/", response_model=EmpleadoResponse, status_code=status.HTTP_201_CREATED)
def crear_empleado(datos: EmpleadoCreate, db: Session = Depends(get_db)):
    nuevo_empleado = Empleado(**datos.model_dump())
    db.add(nuevo_empleado)
    db.commit()
    db.refresh(nuevo_empleado)
    return nuevo_empleado

@router.put("/{id_empleado}", response_model=EmpleadoResponse, status_code=status.HTTP_200_OK)
def actualizar_empleado(id_empleado: int, datos: EmpleadoUpdate, db: Session = Depends(get_db)):
    empleado = db.query(Empleado).filter(Empleado.id_empleado == id_empleado).first()
    if not empleado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado")
    
    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(empleado, key, value)
        
    db.commit()
    db.refresh(empleado)
    return empleado

@router.delete("/{id_empleado}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_empleado(id_empleado: int, db: Session = Depends(get_db)):
    empleado = db.query(Empleado).filter(Empleado.id_empleado == id_empleado).first()
    if not empleado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado")
    
    db.delete(empleado)
    db.commit()
    return None