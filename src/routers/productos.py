from fastapi import APIRouter, HTTPException

from src.constants.http_status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from src.crud.producto_crud import ProductoCRUD
from src.schemas.producto import (
    ProductoCreate,
    ProductoResponse,
    ProductoUpdate,
)


router = APIRouter()

producto_crud = ProductoCRUD()


@router.get("/productos", response_model=list[ProductoResponse])
def listar_productos():
    productos = producto_crud.listar()

    return [
        ProductoResponse(
            id=producto[0],
            nombre=producto[1],
            descripcion=producto[2],
            categoria=producto[3],
            precio=producto[4],
        )
        for producto in productos
    ]


@router.get("/productos/{id}", response_model=ProductoResponse)
def obtener_producto(id: int):
    try:
        producto = producto_crud.obtener(id)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return ProductoResponse(
        id=id,
        nombre=producto[0],
        descripcion=producto[1],
        categoria=producto[2],
        precio=producto[3],
    )


@router.post(
    "/productos",
    response_model=ProductoResponse,
    status_code=HTTP_201_CREATED,
)
def crear_producto(producto: ProductoCreate):
    try:
        id_producto = producto_crud.crear(
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            categoria=producto.categoria,
            precio=producto.precio,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    return ProductoResponse(
        id=id_producto,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        categoria=producto.categoria,
        precio=producto.precio,
    )


@router.put(
    "/productos/{id}",
    response_model=ProductoResponse,
    status_code=HTTP_200_OK,
)
def actualizar_producto(id: int, producto: ProductoUpdate):
    try:
        producto_crud.actualizar(
            identificador=id,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            categoria=producto.categoria,
            precio=producto.precio,
        )
    except ValueError as error:
        if "No existe un producto" in str(error):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error

        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    return ProductoResponse(
        id=id,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        categoria=producto.categoria,
        precio=producto.precio,
    )


@router.delete(
    "/productos/{id}",
    status_code=HTTP_200_OK,
    responses={
        HTTP_404_NOT_FOUND: {
            "description": "Producto no encontrado"
        },
        HTTP_409_CONFLICT: {
            "description": "No se puede eliminar el producto"
        },
    },
)
def eliminar_producto(id: int):
    try:
        producto_crud.eliminar(id)
    except ValueError as error:
        if "incluido en algun pedido" in str(error):
            raise HTTPException(
                status_code=HTTP_409_CONFLICT,
                detail=str(error),
            ) from error

        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return {
        "mensaje": f"Producto con ID {id} eliminado correctamente"
    }