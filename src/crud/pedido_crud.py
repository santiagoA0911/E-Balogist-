from datetime import date
from decimal import Decimal

from sqlalchemy import func, select

from src.database.connection import SessionLocal
# Se importan las cuatro entidades aunque no todas se usen aqui: SQLAlchemy
# necesita tenerlas registradas para resolver los relationship() entre ellas.
from src.entities.cliente import Cliente
from src.entities.detalle_pedido import DetallePedido
from src.entities.pedido import Pedido
from src.entities.producto import Producto


class PedidoCRUD:
    """CRUD de pedidos sobre SQLAlchemy. El valor_total nunca se digita: se recalcula."""

    columns = ("id", "cliente_id", "fecha", "fecha_entrega", "estado", "direccion_entrega", "valor_total")
    ESTADOS = Pedido.ESTADOS

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def listar(self):
        with self.session_factory() as sesion:
            filas = sesion.execute(
                select(
                    Pedido.id,
                    Pedido.cliente_id,
                    Pedido.fecha,
                    Pedido.fecha_entrega,
                    Pedido.estado,
                    Pedido.direccion_entrega,
                    Pedido.valor_total,
                ).order_by(Pedido.id)
            ).all()
        return [tuple(fila) for fila in filas]

    def obtener(self, identificador):
        id_pedido = self._convertir_id(identificador)
        with self.session_factory() as sesion:
            pedido = self._buscar(sesion, id_pedido)
            return (
                pedido.cliente_id,
                self._texto_fecha(pedido.fecha),
                self._texto_fecha(pedido.fecha_entrega),
                pedido.estado,
                pedido.direccion_entrega,
                pedido.valor_total,
            )

    def crear(self, cliente_id, fecha, fecha_entrega, estado, direccion_entrega):
        id_cliente = self._convertir_id(cliente_id)
        fecha_pedido = self._convertir_fecha(fecha, obligatoria=True)
        fecha_de_entrega = self._convertir_fecha(fecha_entrega, obligatoria=False)
        self._validar_estado(estado)
        with self.session_factory() as sesion:
            self._validar_cliente(sesion, id_cliente)
            pedido = Pedido(
                cliente_id=id_cliente,
                fecha=fecha_pedido,
                fecha_entrega=fecha_de_entrega,
                estado=estado,
                direccion_entrega=direccion_entrega,
                valor_total=Decimal("0"),
            )
            sesion.add(pedido)
            sesion.commit()
            return pedido.id

    def actualizar(self, identificador, cliente_id, fecha, fecha_entrega, estado, direccion_entrega):
        id_pedido = self._convertir_id(identificador)
        id_cliente = self._convertir_id(cliente_id)
        fecha_pedido = self._convertir_fecha(fecha, obligatoria=True)
        fecha_de_entrega = self._convertir_fecha(fecha_entrega, obligatoria=False)
        self._validar_estado(estado)
        with self.session_factory() as sesion:
            pedido = self._buscar(sesion, id_pedido)
            self._validar_cliente(sesion, id_cliente)
            pedido.cliente_id = id_cliente
            pedido.fecha = fecha_pedido
            pedido.fecha_entrega = fecha_de_entrega
            pedido.estado = estado
            pedido.direccion_entrega = direccion_entrega
            sesion.commit()

    def eliminar(self, identificador):
        id_pedido = self._convertir_id(identificador)
        with self.session_factory() as sesion:
            pedido = self._buscar(sesion, id_pedido)
            sesion.delete(pedido)
            sesion.commit()

    def recalcular_total(self, pedido_id):
        id_pedido = self._convertir_id(pedido_id)
        with self.session_factory() as sesion:
            pedido = self._buscar(sesion, id_pedido)
            total = self.calcular_total(sesion, id_pedido)
            pedido.valor_total = total
            sesion.commit()
            return total

    def existe(self, pedido_id):
        id_pedido = self._convertir_id(pedido_id)
        with self.session_factory() as sesion:
            return sesion.get(Pedido, id_pedido) is not None

    @staticmethod
    def calcular_total(sesion, id_pedido):
        """Suma cantidad * precio_unitario de los detalles del pedido dentro de la sesion dada."""
        total = sesion.execute(
            select(
                func.coalesce(func.sum(DetallePedido.cantidad * DetallePedido.precio_unitario), 0)
            ).where(DetallePedido.pedido_id == id_pedido)
        ).scalar_one()
        return Decimal(str(total if total is not None else 0))

    @staticmethod
    def _buscar(sesion, id_pedido):
        pedido = sesion.get(Pedido, id_pedido)
        if pedido is None:
            raise ValueError(f"No existe un pedido con el ID {id_pedido}.")
        return pedido

    @staticmethod
    def _validar_cliente(sesion, id_cliente):
        if sesion.get(Cliente, id_cliente) is None:
            raise ValueError("El cliente indicado no existe.")

    @classmethod
    def _validar_estado(cls, estado):
        if estado not in cls.ESTADOS:
            raise ValueError(f"Estado no valido. Usa uno de: {', '.join(cls.ESTADOS)}.")

    @staticmethod
    def _convertir_id(identificador):
        try:
            return int(identificador)
        except (TypeError, ValueError) as error:
            raise ValueError("El ID debe ser un numero entero.") from error

    @staticmethod
    def _convertir_fecha(valor, obligatoria):
        if isinstance(valor, date):
            return valor
        texto = (valor or "").strip()
        if not texto:
            if obligatoria:
                raise ValueError("La fecha debe tener el formato AAAA-MM-DD.")
            return None
        try:
            return date.fromisoformat(texto)
        except ValueError as error:
            raise ValueError("La fecha debe tener el formato AAAA-MM-DD.") from error

    @staticmethod
    def _texto_fecha(valor):
        return valor.isoformat() if valor else ""
