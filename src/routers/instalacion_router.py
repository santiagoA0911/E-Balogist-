from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database.connection import get_db
from src.entities.instalacion import Instalacion
from src.schemas.instalacion_schema import InstalacionCreate, InstalacionUpdate, InstalacionResponse

router = APIRouter(prefix="/instalaciones", tags=["Instalaciones"])

@router.get("/", response_model=List[InstalacionResponse], status_code=status.HTTP_200_OK)
def listar_instalaciones(db: Session = Depends(get_db)):
    return db.query(Instalacion).all()

@router.get("/{id_instalacion}", response_model=InstalacionResponse, status_code=status.HTTP_200_OK)
def obtener_instalacion(id_instalacion: int, db: Session = Depends(get_db)):
    inst = db.query(Instalacion).filter(Instalacion.id_instalacion == id_instalacion).first()
    if not inst:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instalación no encontrada")
    return inst

@router.post("/", response_model=InstalacionResponse, status_code=status.HTTP_201_CREATED)
def crear_instalacion(datos: InstalacionCreate, db: Session = Depends(get_db)):
    nueva_inst = Instalacion(**datos.model_dump())
    db.add(nueva_inst)
    db.commit()
    db.refresh(nueva_inst)
    return nueva_inst

@router.put("/{id_instalacion}", response_model=InstalacionResponse, status_code=status.HTTP_200_OK)
def actualizar_instalacion(id_instalacion: int, datos: InstalacionUpdate, db: Session = Depends(get_db)):
    inst = db.query(Instalacion).filter(Instalacion.id_instalacion == id_instalacion).first()
    if not inst:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instalación no encontrada")
    
    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(inst, key, value)
        
    db.commit()
    db.refresh(inst)
    return inst

@router.delete("/{id_instalacion}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_instalacion(id_instalacion: int, db: Session = Depends(get_db)):
    inst = db.query(Instalacion).filter(Instalacion.id_instalacion == id_instalacion).first()
    if not inst:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instalación no encontrada")
    
    db.delete(inst)
    db.commit()
    return None