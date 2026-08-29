import sqlite3
from uuid import uuid4


class ProductoCRUD:
    columns = ("id_producto", "nombre", "descripcion", "categoria", "precio")

    def __init__(self, database):
        self.database = database

    def listar(self):
        return self.database.rows("SELECT id_producto, nombre, descripcion, categoria, precio FROM productos")

    def obtener(self, id_producto):
        return self.database.rows(
            "SELECT nombre, descripcion, categoria, precio FROM productos WHERE id_producto = ?",
            (id_producto,),
        )[0]

    def crear(self, nombre, descripcion, categoria, precio):
        id_producto = str(uuid4())
        self.database.run(
            "INSERT INTO productos VALUES (?, ?, ?, ?, ?)",
            (id_producto, nombre, descripcion, categoria, precio),
        )
        return id_producto

    def actualizar(self, id_producto, nombre, descripcion, categoria, precio):
        self.database.run(
            "UPDATE productos SET nombre=?, descripcion=?, categoria=?, precio=? WHERE id_producto=?",
            (nombre, descripcion, categoria, precio, id_producto),
        )

    def eliminar(self, id_producto):
        try:
            self.database.run("DELETE FROM productos WHERE id_producto=?", (id_producto,))
        except sqlite3.IntegrityError as error:
            raise ValueError("No se puede eliminar: el producto está incluido en algún pedido.") from error
