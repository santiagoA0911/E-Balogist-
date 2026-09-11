from decimal import Decimal, InvalidOperation

from sqlalchemy import func, select

from src.database.connection import SessionLocal
# Se importan las cuatro entidades aunque no todas se usen aqui: SQLAlchemy
# necesita tenerlas registradas para resolver los relationship() entre ellas.
from src.entities.cliente import Cliente
from src.entities.detalle_pedido import DetallePedido
from src.entities.pedido import Pedido
from src.entities.producto import Producto


class ProductoCRUD:
    """CRUD de productos sobre SQLAlchemy. El precio se guarda siempre como Decimal."""

    columns = ("id", "nombre", "descripcion", "categoria", "precio")

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def listar(self):
        with self.session_factory() as sesion:
            filas = sesion.execute(
                select(
                    Producto.id,
                    Producto.nombre,
                    Producto.descripcion,
                    Producto.categoria,
                    Producto.precio,
                ).order_by(Producto.id)
            ).all()
        return [tuple(fila) for fila in filas]

    def obtener(self, identificador):
        id_producto = self._convertir_id(identificador)
        with self.session_factory() as sesion:
            producto = self._buscar(sesion, id_producto)
            return (
                producto.nombre,
                producto.descripcion,
                producto.categoria,
                producto.precio,
            )

    def crear(self, nombre, descripcion, categoria, precio):
        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            categoria=categoria,
            precio=self._convertir_precio(precio),
        )
        with self.session_factory() as sesion:
            sesion.add(producto)
            sesion.commit()
            return producto.id

    def actualizar(self, identificador, nombre, descripcion, categoria, precio):
        id_producto = self._convertir_id(identificador)
        nuevo_precio = self._convertir_precio(precio)
        with self.session_factory() as sesion:
            producto = self._buscar(sesion, id_producto)
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.categoria = categoria
            producto.precio = nuevo_precio
            sesion.commit()

    def eliminar(self, identificador):
        id_producto = self._convertir_id(identificador)
        with self.session_factory() as sesion:
            producto = self._buscar(sesion, id_producto)
            detalles = sesion.execute(
                select(func.count(DetallePedido.id)).where(DetallePedido.producto_id == id_producto)
            ).scalar_one()
            if detalles:
                raise ValueError("No se puede eliminar: el producto esta incluido en algun pedido.")
            sesion.delete(producto)
            sesion.commit()

    @staticmethod
    def _buscar(sesion, id_producto):
        producto = sesion.get(Producto, id_producto)
        if producto is None:
            raise ValueError(f"No existe un producto con el ID {id_producto}.")
        return producto

    @staticmethod
    def _convertir_id(identificador):
        try:
            return int(identificador)
        except (TypeError, ValueError) as error:
            raise ValueError("El ID debe ser un numero entero.") from error

    @staticmethod
    def _convertir_precio(precio):
        try:
            valor = Decimal(str(precio))
        except (InvalidOperation, TypeError, ValueError) as error:
            raise ValueError("El precio debe ser un numero valido.") from error
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        return valor
