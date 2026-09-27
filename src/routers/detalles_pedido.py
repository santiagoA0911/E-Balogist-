from fastapi import APIRouter, HTTPException

from src.constants.http_status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from src.crud.detalle_pedido_crud import DetallePedidoCRUD
from src.schemas.detalle_pedido import (
    DetallePedidoCreate,
    DetallePedidoResponse,
    DetallePedidoUpdate,
)


router = APIRouter()

detalle_pedido_crud = DetallePedidoCRUD()


@router.get(
    "/detalles-pedido/{pedido_id}",
    response_model=list[DetallePedidoResponse],
)
def listar_detalles_pedido(pedido_id: int):
    detalles = detalle_pedido_crud.listar_por_pedido(pedido_id)

    return [
    DetallePedidoResponse(
        id=detalle[0],
        pedido_id=pedido_id,
        producto_id=detalle[1],
        cantidad=float(detalle[2]),
        precio_unitario=float(detalle[3]),
        subtotal=float(detalle[4]),
    )
    for detalle in detalles
]


@router.get(
    "/detalles-pedido/item/{id}",
    response_model=DetallePedidoResponse,
)
def obtener_detalle_pedido(id: int):
    try:
        detalle = detalle_pedido_crud.obtener(id)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    pedido_id = detalle[0]
    producto_id = detalle[1]
    cantidad = float(detalle[2])
    precio_unitario = float(detalle[3])

    return DetallePedidoResponse(
        id=id,
        pedido_id=pedido_id,
        producto_id=producto_id,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        subtotal=cantidad * precio_unitario,
    )


@router.post(
    "/detalles-pedido",
    response_model=DetallePedidoResponse,
    status_code=HTTP_201_CREATED,
)
def crear_detalle_pedido(detalle: DetallePedidoCreate):
    try:
        id_detalle = detalle_pedido_crud.crear(
            pedido_id=detalle.pedido_id,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    detalle_creado = detalle_pedido_crud.obtener(id_detalle)

    pedido_id = detalle_creado[0]
    producto_id = detalle_creado[1]
    cantidad = float(detalle_creado[2])
    precio_unitario = float(detalle_creado[3])

    return DetallePedidoResponse(
        id=id_detalle,
        pedido_id=pedido_id,
        producto_id=producto_id,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        subtotal=cantidad * precio_unitario,
    )


@router.put(
    "/detalles-pedido/{id}",
    response_model=DetallePedidoResponse,
    status_code=HTTP_200_OK,
)
def actualizar_detalle_pedido(
    id: int,
    detalle: DetallePedidoUpdate,
):
    try:
        detalle_pedido_crud.actualizar(
            identificador=id,
            cantidad=detalle.cantidad,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    detalle_actualizado = detalle_pedido_crud.obtener(id)

    pedido_id = detalle_actualizado[0]
    producto_id = detalle_actualizado[1]
    cantidad = float(detalle_actualizado[2])
    precio_unitario = float(detalle_actualizado[3])

    return DetallePedidoResponse(
        id=id,
        pedido_id=pedido_id,
        producto_id=producto_id,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        subtotal=cantidad * precio_unitario,
    )


@router.delete(
    "/detalles-pedido/{id}",
    status_code=HTTP_200_OK,
    responses={
        HTTP_404_NOT_FOUND: {
            "description": "Detalle de pedido no encontrado"
        },
        HTTP_409_CONFLICT: {
            "description": "No se puede eliminar el detalle"
        },
    },
)
def eliminar_detalle_pedido(id: int):
    try:
        detalle_pedido_crud.eliminar(id)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return {
        "mensaje": f"Detalle de pedido con ID {id} eliminado correctamente"
    }