from http import HTTPStatus
from pathlib import Path

from fastapi import APIRouter, HTTPException

from api.schemas import CompraCreate, CompraList, CompraRead, CompraUpdate, compraPost, compraPut
from crud.compra_crud import CompraCRUD
from crud.database import Database

compra_db = Database(Path(__file__).resolve().parents[1] / "database.sqlite3")
compra_crud = CompraCRUD(compra_db)

compra_router = APIRouter(prefix="/compras", tags=["compras"])


def _compra_to_dict(compra):
    return {
        "id_compra": compra[0],
        "fecha": compra[1],
        "valor_total": compra[2],
        "estado": compra[3],
        "id_proveedor": compra[4],
    }

@compra_router.get("/", response_model=CompraList)
def listar_compras():
    compras = compra_crud.listar()
    if not compras:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No se encontraron compras")
    return {
        "data": [_compra_to_dict(compra) for compra in compras],
        "status": HTTPStatus.OK,
        "message": "Compras listadas correctamente",
    }


@compra_router.get("/{id_compra}", response_model=CompraRead)
def obtener_compra(id_compra: str):
    compra = compra_crud.obtener(id_compra)
    if not compra:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Compra no encontrada")
    return _compra_to_dict(compra)


@compra_router.post("/", response_model=compraPost, status_code=HTTPStatus.CREATED)
def crear_compra(compra: CompraCreate):
    id_compra = compra_crud.crear(
        compra.fecha,
        compra.valor_total,
        compra.estado,
        str(compra.id_proveedor) if compra.id_proveedor else None,
    )
    compra_creada = compra_crud.obtener(id_compra)
    return {
        "data": _compra_to_dict(compra_creada),
        "status": HTTPStatus.CREATED,
        "message": "Compra creada correctamente",
    }


@compra_router.put("/{id_compra}", response_model=compraPut)
def actualizar_compra(id_compra: str, compra: CompraUpdate):
    compra_actual = compra_crud.obtener(id_compra)
    if not compra_actual:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Compra no encontrada")

    compra_crud.actualizar(
        id_compra,
        compra.fecha if compra.fecha is not None else compra_actual[1],
        compra.valor_total if compra.valor_total is not None else compra_actual[2],
        compra.estado if compra.estado is not None else compra_actual[3],
        str(compra.id_proveedor) if compra.id_proveedor is not None else compra_actual[4],
    )

    compra_actualizada = compra_crud.obtener(id_compra)
    return {
        "data": _compra_to_dict(compra_actualizada),
        "status": HTTPStatus.OK,
        "message": "Compra actualizada correctamente",
    }


@compra_router.delete("/{id_compra}")
def eliminar_compra(id_compra: str):
    compra = compra_crud.obtener(id_compra)
    if not compra:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Compra no encontrada")

    compra_crud.eliminar(id_compra)
    return {
        "status": HTTPStatus.OK,
        "message": "Compra eliminada correctamente",
    }
