from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database.connection import get_db
from src.entities.produccion import Produccion
from src.schemas.produccion_schema import ProduccionCreate, ProduccionUpdate, ProduccionResponse

router = APIRouter(prefix="/producciones", tags=["Producción"])

@router.get("/", response_model=List[ProduccionResponse], status_code=status.HTTP_200_OK)
def listar_producciones(db: Session = Depends(get_db)):
    return db.query(Produccion).all()

@router.get("/{id_produccion}", response_model=ProduccionResponse, status_code=status.HTTP_200_OK)
def obtener_produccion(id_produccion: int, db: Session = Depends(get_db)):
    prod = db.query(Produccion).filter(Produccion.id_produccion == id_produccion).first()
    if not prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producción no encontrada")
    return prod

@router.post("/", response_model=ProduccionResponse, status_code=status.HTTP_201_CREATED)
def crear_produccion(datos: ProduccionCreate, db: Session = Depends(get_db)):
    nueva_prod = Produccion(**datos.model_dump())
    db.add(nueva_prod)
    db.commit()
    db.refresh(nueva_prod)
    return nueva_prod

@router.put("/{id_produccion}", response_model=ProduccionResponse, status_code=status.HTTP_200_OK)
def actualizar_produccion(id_produccion: int, datos: ProduccionUpdate, db: Session = Depends(get_db)):
    prod = db.query(Produccion).filter(Produccion.id_produccion == id_produccion).first()
    if not prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producción no encontrada")
    
    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(prod, key, value)
        
    db.commit()
    db.refresh(prod)
    return prod

@router.delete("/{id_produccion}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_produccion(id_produccion: int, db: Session = Depends(get_db)):
    prod = db.query(Produccion).filter(Produccion.id_produccion == id_produccion).first()
    if not prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producción no encontrada")
    
    db.delete(prod)
    db.commit()
    return None