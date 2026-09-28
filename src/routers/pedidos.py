from fastapi import APIRouter, HTTPException

from src.constants.http_status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from src.crud.pedido_crud import PedidoCRUD
from src.schemas.pedido import (
    PedidoCreate,
    PedidoResponse,
    PedidoUpdate,
)


router = APIRouter()

pedido_crud = PedidoCRUD()


@router.get("/pedidos", response_model=list[PedidoResponse])
def listar_pedidos():
    pedidos = pedido_crud.listar()

    return [
        PedidoResponse(
            id=pedido[0],
            cliente_id=pedido[1],
            fecha=pedido[2].isoformat(),
            fecha_entrega=pedido[3].isoformat() if pedido[3] else "",
            estado=pedido[4],
            direccion_entrega=pedido[5],
            valor_total=float(pedido[6]),
        )
        for pedido in pedidos
    ]


@router.get("/pedidos/{id}", response_model=PedidoResponse)
def obtener_pedido(id: int):
    try:
        pedido = pedido_crud.obtener(id)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return PedidoResponse(
        id=id,
        cliente_id=pedido[0],
        fecha=pedido[1],
        fecha_entrega=pedido[2],
        estado=pedido[3],
        direccion_entrega=pedido[4],
        valor_total=float(pedido[5]),
    )


@router.post(
    "/pedidos",
    response_model=PedidoResponse,
    status_code=HTTP_201_CREATED,
)
def crear_pedido(pedido: PedidoCreate):
    try:
        id_pedido = pedido_crud.crear(
            cliente_id=pedido.cliente_id,
            fecha=pedido.fecha,
            fecha_entrega=pedido.fecha_entrega,
            estado=pedido.estado,
            direccion_entrega=pedido.direccion_entrega,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    pedido_creado = pedido_crud.obtener(id_pedido)

    return PedidoResponse(
        id=id_pedido,
        cliente_id=pedido_creado[0],
        fecha=pedido_creado[1],
        fecha_entrega=pedido_creado[2],
        estado=pedido_creado[3],
        direccion_entrega=pedido_creado[4],
        valor_total=float(pedido_creado[5]),
    )


@router.put(
    "/pedidos/{id}",
    response_model=PedidoResponse,
    status_code=HTTP_200_OK,
)
def actualizar_pedido(id: int, pedido: PedidoUpdate):
    try:
        pedido_crud.actualizar(
            identificador=id,
            cliente_id=pedido.cliente_id,
            fecha=pedido.fecha,
            fecha_entrega=pedido.fecha_entrega,
            estado=pedido.estado,
            direccion_entrega=pedido.direccion_entrega,
        )
    except ValueError as error:
        mensaje = str(error)

        if "No existe un pedido" in mensaje:
            codigo = HTTP_404_NOT_FOUND
        else:
            codigo = HTTP_409_CONFLICT

        raise HTTPException(
            status_code=codigo,
            detail=mensaje,
        ) from error

    pedido_actualizado = pedido_crud.obtener(id)

    return PedidoResponse(
        id=id,
        cliente_id=pedido_actualizado[0],
        fecha=pedido_actualizado[1],
        fecha_entrega=pedido_actualizado[2],
        estado=pedido_actualizado[3],
        direccion_entrega=pedido_actualizado[4],
        valor_total=float(pedido_actualizado[5]),
    )


@router.delete(
    "/pedidos/{id}",
    status_code=HTTP_200_OK,
    responses={
        HTTP_404_NOT_FOUND: {
            "description": "Pedido no encontrado"
        },
        HTTP_409_CONFLICT: {
            "description": "No se puede eliminar el pedido"
        },
    },
)
def eliminar_pedido(id: int):
    try:
        pedido_crud.eliminar(id)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return {
        "mensaje": f"Pedido con ID {id} eliminado correctamente"
    }