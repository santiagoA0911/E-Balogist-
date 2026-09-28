from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from src.database.connection import SessionLocal
# Se importan las cuatro entidades aunque no todas se usen aqui: SQLAlchemy
# necesita tenerlas registradas para resolver los relationship() entre ellas.
from src.entities.cliente import Cliente
from src.entities.detalle_pedido import DetallePedido
from src.entities.pedido import Pedido
from src.entities.producto import Producto


class ClienteCRUD:
    """CRUD de clientes sobre SQLAlchemy. Cada metodo abre y cierra su propia sesion."""

    columns = ("id", "nombre", "documento", "telefono", "correo", "direccion")

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def listar(self):
        with self.session_factory() as sesion:
            filas = sesion.execute(
                select(
                    Cliente.id,
                    Cliente.nombre,
                    Cliente.documento,
                    Cliente.telefono,
                    Cliente.correo,
                    Cliente.direccion,
                ).order_by(Cliente.id)
            ).all()
        return [tuple(fila) for fila in filas]

    def obtener(self, identificador):
        id_cliente = self._convertir_id(identificador)
        with self.session_factory() as sesion:
            cliente = self._buscar(sesion, id_cliente)
            return (
                cliente.nombre,
                cliente.documento,
                cliente.telefono,
                cliente.correo,
                cliente.direccion,
            )

    def crear(self, nombre, documento, telefono, correo, direccion):
        cliente = Cliente(
            nombre=nombre,
            documento=documento,
            telefono=telefono,
            correo=correo,
            direccion=direccion,
        )
        with self.session_factory() as sesion:
            sesion.add(cliente)
            try:
                sesion.commit()
            except IntegrityError as error:
                sesion.rollback()
                raise ValueError("Ya existe un cliente con ese documento.") from error
            return cliente.id

    def actualizar(self, identificador, nombre, documento, telefono, correo, direccion):
        id_cliente = self._convertir_id(identificador)
        with self.session_factory() as sesion:
            cliente = self._buscar(sesion, id_cliente)
            cliente.nombre = nombre
            cliente.documento = documento
            cliente.telefono = telefono
            cliente.correo = correo
            cliente.direccion = direccion
            try:
                sesion.commit()
            except IntegrityError as error:
                sesion.rollback()
                raise ValueError("Ya existe un cliente con ese documento.") from error

    def eliminar(self, identificador):
        id_cliente = self._convertir_id(identificador)
        with self.session_factory() as sesion:
            cliente = self._buscar(sesion, id_cliente)
            pedidos = sesion.execute(
                select(func.count(Pedido.id)).where(Pedido.cliente_id == id_cliente)
            ).scalar_one()
            if pedidos:
                raise ValueError("No se puede eliminar: el cliente tiene pedidos registrados.")
            sesion.delete(cliente)
            sesion.commit()

    @staticmethod
    def _buscar(sesion, id_cliente):
        cliente = sesion.get(Cliente, id_cliente)
        if cliente is None:
            raise ValueError(f"No existe un cliente con el ID {id_cliente}.")
        return cliente

    @staticmethod
    def _convertir_id(identificador):
        try:
            return int(identificador)
        except (TypeError, ValueError) as error:
            raise ValueError("El ID debe ser un numero entero.") from error
