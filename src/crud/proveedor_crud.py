from uuid import uuid4


class ProveedorCRUD:
    columns = ("id_proveedor", "nombre", "tel", "direccion", "correo")

    def __init__(self, database):
        self.database = database

    def listar(self):
        return self.database.rows("SELECT id_proveedor, nombre, tel, direccion, correo FROM proveedores")

    def obtener(self, id_proveedor):
        rows = self.database.rows(
            "SELECT id_proveedor, nombre, tel, direccion, correo FROM proveedores WHERE id_proveedor = ?",
            (id_proveedor,),
        )
        return rows[0] if rows else None

    def crear(self, nombre, tel, direccion, correo):
        id_proveedor = str(uuid4())
        self.database.run(
            "INSERT INTO proveedores VALUES (?, ?, ?, ?, ?)",
            (id_proveedor, nombre, tel, direccion, correo),
        )
        return id_proveedor

    def actualizar(self, id_proveedor, nombre, tel, direccion, correo):
        self.database.run(
            "UPDATE proveedores SET nombre=?, tel=?, direccion=?, correo=? WHERE id_proveedor=?",
            (nombre, tel, direccion, correo, id_proveedor),
        )

    def eliminar(self, id_proveedor):
        self.database.run("DELETE FROM proveedores WHERE id_proveedor=?", (id_proveedor,))
