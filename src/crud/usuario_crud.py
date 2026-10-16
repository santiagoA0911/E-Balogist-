
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database.connection import SessionLocal
from src.entities.usuario import Usuario


class UsuarioCRUD:
    """Operaciones CRUD de usuarios usando SQLAlchemy."""

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def listar(self):
        with self.session_factory() as sesion:
            usuarios = sesion.scalars(
                select(Usuario).order_by(Usuario.id)
            ).all()
            return [
                {
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "correo": usuario.correo,
                    "activo": usuario.activo,
                }
                for usuario in usuarios
            ]

    def obtener(self, identificador):
        id_usuario = self._convertir_id(identificador)

        with self.session_factory() as sesion:
            usuario = sesion.get(Usuario, id_usuario)

            if usuario is None:
                raise ValueError(
                    f"No existe un usuario con el ID {id_usuario}."
                )

            return {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                "activo": usuario.activo,
            }

    def crear(self, nombre, correo, activo=True):
        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            activo=activo,
        )

        with self.session_factory() as sesion:
            sesion.add(usuario)

            try:
                sesion.commit()
                sesion.refresh(usuario)
                return usuario.id
            except IntegrityError as error:
                sesion.rollback()
                raise ValueError(
                    "Ya existe un usuario con ese correo electrónico."
                ) from error

    def actualizar(self, identificador, nombre, correo, activo):
        id_usuario = self._convertir_id(identificador)

        with self.session_factory() as sesion:
            usuario = sesion.get(Usuario, id_usuario)

            if usuario is None:
                raise ValueError(
                    f"No existe un usuario con el ID {id_usuario}."
                )

            usuario.nombre = nombre
            usuario.correo = correo
            usuario.activo = activo

            try:
                sesion.commit()
            except IntegrityError as error:
                sesion.rollback()
                raise ValueError(
                    "Ya existe otro usuario con ese correo electrónico."
                ) from error

    def eliminar(self, identificador):
        id_usuario = self._convertir_id(identificador)

        with self.session_factory() as sesion:
            usuario = sesion.get(Usuario, id_usuario)

            if usuario is None:
                raise ValueError(
                    f"No existe un usuario con el ID {id_usuario}."
                )

            sesion.delete(usuario)
            sesion.commit()

    @staticmethod
    def _convertir_id(identificador):
        try:
            return int(identificador)
        except (TypeError, ValueError) as error:
            raise ValueError(
                "El ID debe ser un número entero."
            ) from error
