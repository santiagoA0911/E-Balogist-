from decimal import Decimal, InvalidOperation

from sqlalchemy import select

from src.crud.pedido_crud import PedidoCRUD
from src.database.connection import SessionLocal
# Se importan las cuatro entidades aunque no todas se usen aqui: SQLAlchemy
# necesita tenerlas registradas para resolver los relationship() entre ellas.
from src.entities.cliente import Cliente
from src.entities.detalle_pedido import DetallePedido
from src.entities.pedido import Pedido
from src.entities.producto import Producto


class DetallePedidoCRUD:
    """CRUD de los items de un pedido. Toda escritura recalcula el total del pedido."""

    columns = ("id", "producto", "cantidad", "precio_unitario", "subtotal")

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def listar_por_pedido(self, pedido_id):
        id_pedido = self._convertir_id(pedido_id)
        with self.session_factory() as sesion:
            filas = sesion.execute(
                select(
                    DetallePedido.id,
                    Producto.nombre,
                    DetallePedido.cantidad,
                    DetallePedido.precio_unitario,
                    (DetallePedido.cantidad * DetallePedido.precio_unitario).label("subtotal"),
                )
                .join(Producto, Producto.id == DetallePedido.producto_id)
                .where(DetallePedido.pedido_id == id_pedido)
                .order_by(DetallePedido.id)
            ).all()
        return [tuple(fila) for fila in filas]

    def obtener(self, identificador):
        id_detalle = self._convertir_id(identificador)
        with self.session_factory() as sesion:
            detalle = self._buscar(sesion, id_detalle)
            return (
                detalle.pedido_id,
                detalle.producto_id,
                detalle.cantidad,
                detalle.precio_unitario,
            )

    def crear(self, pedido_id, producto_id, cantidad):
        id_pedido = self._convertir_id(pedido_id)
        id_producto = self._convertir_id(producto_id)
        cantidad_nueva = self._convertir_cantidad(cantidad)
        with self.session_factory() as sesion:
            if sesion.get(Pedido, id_pedido) is None:
                raise ValueError("El pedido indicado no existe.")
            producto = sesion.get(Producto, id_producto)
            if producto is None:
                raise ValueError("El producto indicado no existe.")
            detalle = DetallePedido(
                pedido_id=id_pedido,
                producto_id=id_producto,
                cantidad=cantidad_nueva,
                precio_unitario=Decimal(str(producto.precio or 0)),
            )
            sesion.add(detalle)
            sesion.flush()
            self._recalcular_total(sesion, id_pedido)
            sesion.commit()
            return detalle.id

    def actualizar(self, identificador, cantidad):
        id_detalle = self._convertir_id(identificador)
        cantidad_nueva = self._convertir_cantidad(cantidad)
        with self.session_factory() as sesion:
            detalle = self._buscar(sesion, id_detalle)
            detalle.cantidad = cantidad_nueva
            sesion.flush()
            self._recalcular_total(sesion, detalle.pedido_id)
            sesion.commit()

    def eliminar(self, identificador):
        id_detalle = self._convertir_id(identificador)
        with self.session_factory() as sesion:
            detalle = self._buscar(sesion, id_detalle)
            id_pedido = detalle.pedido_id
            sesion.delete(detalle)
            sesion.flush()
            self._recalcular_total(sesion, id_pedido)
            sesion.commit()

    @staticmethod
    def _recalcular_total(sesion, id_pedido):
        """Deja el valor_total del pedido al dia sin abrir otra sesion."""
        pedido = sesion.get(Pedido, id_pedido)
        if pedido is None:
            raise ValueError("El pedido indicado no existe.")
        pedido.valor_total = PedidoCRUD.calcular_total(sesion, id_pedido)
        return pedido.valor_total

    @staticmethod
    def _buscar(sesion, id_detalle):
        detalle = sesion.get(DetallePedido, id_detalle)
        if detalle is None:
            raise ValueError(f"No existe un item con el ID {id_detalle}.")
        return detalle

    @staticmethod
    def _convertir_id(identificador):
        try:
            return int(identificador)
        except (TypeError, ValueError) as error:
            raise ValueError("El ID debe ser un numero entero.") from error

    @staticmethod
    def _convertir_cantidad(cantidad):
        try:
            valor = Decimal(str(cantidad))
        except (InvalidOperation, TypeError, ValueError) as error:
            raise ValueError("La cantidad debe ser un numero valido.") from error
        if valor <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        return valor
