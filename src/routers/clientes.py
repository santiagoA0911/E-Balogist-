from fastapi import APIRouter, HTTPException

from src.constants.http_status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from src.crud.cliente_crud import ClienteCRUD
from src.schemas.cliente import (
    ClienteCreate,
    ClienteResponse,
    ClienteUpdate,
)


router = APIRouter()

cliente_crud = ClienteCRUD()


@router.get("/clientes", response_model=list[ClienteResponse])
def listar_clientes():
    clientes = cliente_crud.listar()

    return [
        ClienteResponse(
            id=cliente[0],
            nombre=cliente[1],
            documento=cliente[2],
            telefono=cliente[3],
            correo=cliente[4],
            direccion=cliente[5],
        )
        for cliente in clientes
    ]


@router.get("/clientes/{id}", response_model=ClienteResponse)
def obtener_cliente(id: int):
    try:
        cliente = cliente_crud.obtener(id)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return ClienteResponse(
        id=id,
        nombre=cliente[0],
        documento=cliente[1],
        telefono=cliente[2],
        correo=cliente[3],
        direccion=cliente[4],
    )


@router.post(
    "/clientes",
    response_model=ClienteResponse,
    status_code=HTTP_201_CREATED,
)
def crear_cliente(cliente: ClienteCreate):
    try:
        id_cliente = cliente_crud.crear(
            nombre=cliente.nombre,
            documento=cliente.documento,
            telefono=cliente.telefono,
            correo=cliente.correo,
            direccion=cliente.direccion,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    return ClienteResponse(
        id=id_cliente,
        nombre=cliente.nombre,
        documento=cliente.documento,
        telefono=cliente.telefono,
        correo=cliente.correo,
        direccion=cliente.direccion,
    )


@router.put(
    "/clientes/{id}",
    response_model=ClienteResponse,
    status_code=HTTP_200_OK,
)
def actualizar_cliente(id: int, cliente: ClienteUpdate):
    try:
        cliente_crud.actualizar(
            identificador=id,
            nombre=cliente.nombre,
            documento=cliente.documento,
            telefono=cliente.telefono,
            correo=cliente.correo,
            direccion=cliente.direccion,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    return ClienteResponse(
        id=id,
        nombre=cliente.nombre,
        documento=cliente.documento,
        telefono=cliente.telefono,
        correo=cliente.correo,
        direccion=cliente.direccion,
    )
@router.delete(
    "/clientes/{id}",
    status_code=HTTP_200_OK,
    responses={
        HTTP_404_NOT_FOUND: {
            "description": "Cliente no encontrado"
        },
        HTTP_409_CONFLICT: {
            "description": "No se puede eliminar el cliente"
        },
    },
)
def eliminar_cliente(id: int):
    try:
        cliente_crud.eliminar(id)
    except ValueError as error:
        if "pedidos registrados" in str(error):
            raise HTTPException(
                status_code=HTTP_409_CONFLICT,
                detail=str(error),
            ) from error

        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return {
        "mensaje": f"Cliente con ID {id} eliminado correctamente"
    }