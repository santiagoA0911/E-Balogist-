from uuid import UUID, uuid4


class CompraCRUD:
    columns = ("id_compra", "fecha", "valor_total", "estado", "id_proveedor")

    def __init__(self, database):
        self.database = database

    def listar(self):
        return self.database.rows("SELECT id_compra, fecha, valor_total, estado, id_proveedor FROM compras")

    def obtener(self, id_compra):
        return self.database.rows(
            "SELECT fecha, valor_total, estado, id_proveedor FROM compras WHERE id_compra = ?",
            (id_compra,),
        )[0]

    def crear(self, fecha, valor_total, estado, id_proveedor):
        id_compra = str(uuid4())
        self._validar_proveedor(id_proveedor)
        self.database.run(
            "INSERT INTO compras VALUES (?, ?, ?, ?, ?)",
            (id_compra, fecha, valor_total, estado, id_proveedor),
        )
        return id_compra

    def actualizar(self, id_compra, fecha, valor_total, estado, id_proveedor):
        self._validar_proveedor(id_proveedor)
        self.database.run(
            "UPDATE compras SET fecha=?, valor_total=?, estado=?, id_proveedor=? WHERE id_compra=?",
            (fecha, valor_total, estado, id_proveedor, id_compra),
        )

    def eliminar(self, id_compra):
        self.database.run("DELETE FROM compras WHERE id_compra=?", (id_compra,))

    def _validar_proveedor(self, id_proveedor):
        try:
            UUID(id_proveedor)
        except ValueError as error:
            raise ValueError("El ID del proveedor no es un UUID válido.") from error
        if not self.database.rows("SELECT 1 FROM proveedores WHERE id_proveedor=?", (id_proveedor,)):
            raise ValueError("El proveedor indicado no existe.")
