from uuid import UUID, uuid4


class PedidoCRUD:
    columns = ("id_pedido", "id_cliente", "fecha", "fecha_entrega", "estado", "direccion_entrega", "valor_total")
    ESTADOS = ("Pendiente", "En producción", "En tránsito", "Instalado", "Cancelado")

    def __init__(self, database):
        self.database = database

    def listar(self):
        return self.database.rows(
            "SELECT id_pedido, id_cliente, fecha, fecha_entrega, estado, direccion_entrega, valor_total FROM pedidos"
        )

    def obtener(self, id_pedido):
        return self.database.rows(
            "SELECT id_cliente, fecha, fecha_entrega, estado, direccion_entrega, valor_total FROM pedidos WHERE id_pedido = ?",
            (id_pedido,),
        )[0]

    def crear(self, id_cliente, fecha, fecha_entrega, estado, direccion_entrega):
        id_pedido = str(uuid4())
        self._validar_cliente(id_cliente)
        self._validar_estado(estado)
        self.database.run(
            "INSERT INTO pedidos VALUES (?, ?, ?, ?, ?, ?, ?)",
            (id_pedido, id_cliente, fecha, fecha_entrega, estado, direccion_entrega, 0),
        )
        return id_pedido

    def actualizar(self, id_pedido, id_cliente, fecha, fecha_entrega, estado, direccion_entrega):
        self._validar_cliente(id_cliente)
        self._validar_estado(estado)
        self.database.run(
            "UPDATE pedidos SET id_cliente=?, fecha=?, fecha_entrega=?, estado=?, direccion_entrega=? WHERE id_pedido=?",
            (id_cliente, fecha, fecha_entrega, estado, direccion_entrega, id_pedido),
        )

    def eliminar(self, id_pedido):
        self.database.run("DELETE FROM pedidos WHERE id_pedido=?", (id_pedido,))

    def recalcular_total(self, id_pedido):
        self.database.run(
            "UPDATE pedidos SET valor_total = ("
            "    SELECT COALESCE(SUM(cantidad * precio_unitario), 0) FROM detalles_pedido WHERE id_pedido = ?"
            ") WHERE id_pedido = ?",
            (id_pedido, id_pedido),
        )
        return self.database.rows("SELECT valor_total FROM pedidos WHERE id_pedido = ?", (id_pedido,))[0][0]

    def existe(self, id_pedido):
        return bool(self.database.rows("SELECT 1 FROM pedidos WHERE id_pedido=?", (id_pedido,)))

    def _validar_cliente(self, id_cliente):
        try:
            UUID(id_cliente)
        except ValueError as error:
            raise ValueError("El ID del cliente no es un UUID válido.") from error
        if not self.database.rows("SELECT 1 FROM clientes WHERE id_cliente=?", (id_cliente,)):
            raise ValueError("El cliente indicado no existe.")

    def _validar_estado(self, estado):
        if estado not in self.ESTADOS:
            raise ValueError(f"Estado no válido. Usa uno de: {', '.join(self.ESTADOS)}.")
