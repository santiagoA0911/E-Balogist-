from http import HTTPStatus
from pathlib import Path

from fastapi import APIRouter, HTTPException

from schemas.schemas import MaterialCreate, MaterialList, MaterialRead, MaterialUpdate, materialPost, materialPut
from crud.database import Database
from crud.material_crud import MaterialCRUD

material_db = Database(Path(__file__).resolve().parents[1] / "database.sqlite3")
material_crud = MaterialCRUD(material_db)

material_router = APIRouter(prefix="/materiales", tags=["materiales"])


def _material_to_dict(material):
    return {
        "id_material": material[0],
        "nombre": material[1],
        "tipo": material[2],
        "cantidad": material[3],
        "unidad": material[4],
        "precio": material[5],
    }


@material_router.get("/", response_model=MaterialList)
def listar_materiales():
    materiales = material_crud.listar()
    if not materiales:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No se encontraron materiales")
    return {
        "data": [_material_to_dict(material) for material in materiales],
        "status": HTTPStatus.OK,
        "message": "Materiales listados correctamente",
    }


@material_router.get("/{id_material}", response_model=MaterialRead)
def obtener_material(id_material: str):
    material = material_crud.obtener(id_material)
    if not material:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Material no encontrado")
    return _material_to_dict(material)


@material_router.post("/", response_model=materialPost, status_code=HTTPStatus.CREATED)
def crear_material(material: MaterialCreate):
    id_material = material_crud.crear(
        material.nombre,
        material.tipo,
        material.cantidad,
        material.unidad,
        material.precio,
    )
    material_creado = material_crud.obtener(id_material)
    return {
        "data": _material_to_dict(material_creado),
        "status": HTTPStatus.CREATED,
        "message": "Material creado correctamente",
    }


@material_router.put("/{id_material}", response_model=materialPut)
def actualizar_material(id_material: str, material: MaterialUpdate):
    material_actual = material_crud.obtener(id_material)
    if not material_actual:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Material no encontrado")

    material_crud.actualizar(
        id_material,
        material.nombre if material.nombre is not None else material_actual[1],
        material.tipo if material.tipo is not None else material_actual[2],
        material.cantidad if material.cantidad is not None else material_actual[3],
        material.unidad if material.unidad is not None else material_actual[4],
        material.precio if material.precio is not None else material_actual[5],
    )

    material_actualizado = material_crud.obtener(id_material)
    return {
        "data": _material_to_dict(material_actualizado),
        "status": HTTPStatus.OK,
        "message": "Material actualizado correctamente",
    }


@material_router.delete("/{id_material}")
def eliminar_material(id_material: str):
    material = material_crud.obtener(id_material)
    if not material:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Material no encontrado")

    material_crud.eliminar(id_material)
    return {
        "status": HTTPStatus.OK,
        "message": "Material eliminado correctamente",
    }