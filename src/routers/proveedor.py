from http import HTTPStatus
from pathlib import Path

from fastapi import APIRouter, HTTPException

from schemas.schemas import ProveedorCreate, ProveedorList, ProveedorRead, ProveedorUpdate, proveedorPost, proveedorPut
from crud.database import Database
from crud.proveedor_crud import ProveedorCRUD

proveedor_db = Database(Path(__file__).resolve().parents[1] / "database.sqlite3")
proveedor_crud = ProveedorCRUD(proveedor_db)

proveedor_router = APIRouter(prefix="/proveedores", tags=["proveedores"])


def _proveedor_to_dict(proveedor):
    return {
        "id_proveedor": proveedor[0],
        "nombre": proveedor[1],
        "tel": proveedor[2],
        "direccion": proveedor[3],
        "correo": proveedor[4],
    }


@proveedor_router.get("/", response_model=ProveedorList)
def listar_proveedores():
    proveedores = proveedor_crud.listar()
    if not proveedores:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No se encontraron proveedores")
    return {
        "data": [_proveedor_to_dict(proveedor) for proveedor in proveedores],
        "status": HTTPStatus.OK,
        "message": "Proveedores listados correctamente",
    }


@proveedor_router.get("/{id_proveedor}", response_model=ProveedorRead)
def obtener_proveedor(id_proveedor: str):
    proveedor = proveedor_crud.obtener(id_proveedor)
    if not proveedor:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Proveedor no encontrado")
    return _proveedor_to_dict(proveedor)


@proveedor_router.post("/", response_model=proveedorPost, status_code=HTTPStatus.CREATED)
def crear_proveedor(proveedor: ProveedorCreate):
    id_proveedor = proveedor_crud.crear(
        proveedor.nombre,
        proveedor.tel,
        proveedor.direccion,
        proveedor.correo,
    )
    proveedor_creado = proveedor_crud.obtener(id_proveedor)
    return {
        "data": _proveedor_to_dict(proveedor_creado),
        "status": HTTPStatus.CREATED,
        "message": "Proveedor creado correctamente",
    }


@proveedor_router.put("/{id_proveedor}", response_model=proveedorPut)
def actualizar_proveedor(id_proveedor: str, proveedor: ProveedorUpdate):
    proveedor_actual = proveedor_crud.obtener(id_proveedor)
    if not proveedor_actual:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Proveedor no encontrado")

    proveedor_crud.actualizar(
        id_proveedor,
        proveedor.nombre if proveedor.nombre is not None else proveedor_actual[1],
        proveedor.tel if proveedor.tel is not None else proveedor_actual[2],
        proveedor.direccion if proveedor.direccion is not None else proveedor_actual[3],
        proveedor.correo if proveedor.correo is not None else proveedor_actual[4],
    )

    proveedor_actualizado = proveedor_crud.obtener(id_proveedor)
    return {
        "data": _proveedor_to_dict(proveedor_actualizado),
        "status": HTTPStatus.OK,
        "message": "Proveedor actualizado correctamente",
    }


@proveedor_router.delete("/{id_proveedor}")
def eliminar_proveedor(id_proveedor: str):
    proveedor = proveedor_crud.obtener(id_proveedor)
    if not proveedor:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Proveedor no encontrado")

    proveedor_crud.eliminar(id_proveedor)
    return {
        "status": HTTPStatus.OK,
        "message": "Proveedor eliminado correctamente",
    }
