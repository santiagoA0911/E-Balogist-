from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database.connection import get_db
from src.entities.transporte import Transporte
from src.schemas.transporte_schema import TransporteCreate, TransporteUpdate, TransporteResponse

router = APIRouter(prefix="/transportes", tags=["Transporte"])

@router.get("/", response_model=List[TransporteResponse], status_code=status.HTTP_200_OK)
def listar_transportes(db: Session = Depends(get_db)):
    return db.query(Transporte).all()

@router.get("/{id_transporte}", response_model=TransporteResponse, status_code=status.HTTP_200_OK)
def obtener_transporte(id_transporte: int, db: Session = Depends(get_db)):
    trans = db.query(Transporte).filter(Transporte.id_transporte == id_transporte).first()
    if not trans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transporte no encontrado")
    return trans

@router.post("/", response_model=TransporteResponse, status_code=status.HTTP_201_CREATED)
def crear_transporte(datos: TransporteCreate, db: Session = Depends(get_db)):
    nuevo_trans = Transporte(**datos.model_dump())
    db.add(nuevo_trans)
    db.commit()
    db.refresh(nuevo_trans)
    return nuevo_trans

@router.put("/{id_transporte}", response_model=TransporteResponse, status_code=status.HTTP_200_OK)
def actualizar_transporte(id_transporte: int, datos: TransporteUpdate, db: Session = Depends(get_db)):
    trans = db.query(Transporte).filter(Transporte.id_transporte == id_transporte).first()
    if not trans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transporte no encontrado")
    
    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(trans, key, value)
        
    db.commit()
    db.refresh(trans)
    return trans

@router.delete("/{id_transporte}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_transporte(id_transporte: int, db: Session = Depends(get_db)):
    trans = db.query(Transporte).filter(Transporte.id_transporte == id_transporte).first()
    if not trans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transporte no encontrado")
    
    db.delete(trans)
    db.commit()
    return None