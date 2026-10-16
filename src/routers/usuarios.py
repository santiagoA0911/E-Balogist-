from fastapi import APIRouter, HTTPException, status

from src.crud.usuario_crud import UsuarioCRUD
from src.schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
usuario_crud = UsuarioCRUD()


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios():
    return usuario_crud.listar()


@router.get("/{id_usuario}", response_model=UsuarioResponse)
def obtener_usuario(id_usuario: int):
    try:
        return usuario_crud.obtener(id_usuario)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_usuario(datos: UsuarioCreate):
    try:
        id_usuario = usuario_crud.crear(
            nombre=datos.nombre,
            correo=datos.correo,
            activo=datos.activo,
        )
        return usuario_crud.obtener(id_usuario)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put("/{id_usuario}", response_model=UsuarioResponse)
def actualizar_usuario(id_usuario: int, datos: UsuarioUpdate):
    try:
        usuario_crud.actualizar(
            identificador=id_usuario,
            nombre=datos.nombre,
            correo=datos.correo,
            activo=datos.activo,
        )
        return usuario_crud.obtener(id_usuario)
    except ValueError as error:
        mensaje = str(error)
        codigo = (
            status.HTTP_404_NOT_FOUND
            if "No existe" in mensaje
            else status.HTTP_409_CONFLICT
        )
        raise HTTPException(
            status_code=codigo,
            detail=mensaje,
        ) from error


@router.delete("/{id_usuario}")
def eliminar_usuario(id_usuario: int):
    try:
        usuario_crud.eliminar(id_usuario)
        return {"mensaje": f"Usuario {id_usuario} eliminado correctamente."}
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error