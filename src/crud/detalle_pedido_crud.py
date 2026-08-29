from uuid import UUID, uuid4


class DetallePedidoCRUD:
    columns = ("id_detalle", "producto", "cantidad", "precio_unitario", "subtotal")

    def __init__(self, database, pedidos):
        self.database = database
        self.pedidos = pedidos

    def listar_por_pedido(self, id_pedido):
        return self.database.rows(
            "SELECT d.id_detalle, p.nombre, d.cantidad, d.precio_unitario, d.cantidad * d.precio_unitario "
            "FROM detalles_pedido d JOIN productos p ON p.id_producto = d.id_producto "
            "WHERE d.id_pedido = ?",
            (id_pedido,),
        )

    def obtener(self, id_detalle):
        return self.database.rows(
            "SELECT id_pedido, id_producto, cantidad, precio_unitario FROM detalles_pedido WHERE id_detalle = ?",
            (id_detalle,),
        )[0]

    def crear(self, id_pedido, id_producto, cantidad):
        id_detalle = str(uuid4())
        self._validar_pedido(id_pedido)
        precio_unitario = self._precio_del_producto(id_producto)
        self._validar_cantidad(cantidad)
        self.database.run(
            "INSERT INTO detalles_pedido VALUES (?, ?, ?, ?, ?)",
            (id_detalle, id_pedido, id_producto, cantidad, precio_unitario),
        )
        self.pedidos.recalcular_total(id_pedido)
        return id_detalle

    def actualizar(self, id_detalle, cantidad):
        self._validar_cantidad(cantidad)
        id_pedido = self.obtener(id_detalle)[0]
        self.database.run("UPDATE detalles_pedido SET cantidad=? WHERE id_detalle=?", (cantidad, id_detalle))
        self.pedidos.recalcular_total(id_pedido)

    def eliminar(self, id_detalle):
        id_pedido = self.obtener(id_detalle)[0]
        self.database.run("DELETE FROM detalles_pedido WHERE id_detalle=?", (id_detalle,))
        self.pedidos.recalcular_total(id_pedido)

    def _validar_pedido(self, id_pedido):
        try:
            UUID(id_pedido)
        except ValueError as error:
            raise ValueError("El ID del pedido no es un UUID válido.") from error
        if not self.pedidos.existe(id_pedido):
            raise ValueError("El pedido indicado no existe.")

    def _validar_cantidad(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

    def _precio_del_producto(self, id_producto):
        try:
            UUID(id_producto)
        except ValueError as error:
            raise ValueError("El ID del producto no es un UUID válido.") from error
        fila = self.database.rows("SELECT precio FROM productos WHERE id_producto=?", (id_producto,))
        if not fila:
            raise ValueError("El producto indicado no existe.")
        return fila[0][0]
