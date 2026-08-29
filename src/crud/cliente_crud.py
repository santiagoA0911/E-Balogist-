import sqlite3
from uuid import uuid4


class ClienteCRUD:
    columns = ("id_cliente", "nombre", "documento", "telefono", "correo", "direccion")

    def __init__(self, database):
        self.database = database

    def listar(self):
        return self.database.rows("SELECT id_cliente, nombre, documento, telefono, correo, direccion FROM clientes")

    def obtener(self, id_cliente):
        return self.database.rows(
            "SELECT nombre, documento, telefono, correo, direccion FROM clientes WHERE id_cliente = ?",
            (id_cliente,),
        )[0]

    def crear(self, nombre, documento, telefono, correo, direccion):
        id_cliente = str(uuid4())
        try:
            self.database.run(
                "INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?)",
                (id_cliente, nombre, documento, telefono, correo, direccion),
            )
        except sqlite3.IntegrityError as error:
            raise ValueError("Ya existe un cliente con ese documento.") from error
        return id_cliente

    def actualizar(self, id_cliente, nombre, documento, telefono, correo, direccion):
        try:
            self.database.run(
                "UPDATE clientes SET nombre=?, documento=?, telefono=?, correo=?, direccion=? WHERE id_cliente=?",
                (nombre, documento, telefono, correo, direccion, id_cliente),
            )
        except sqlite3.IntegrityError as error:
            raise ValueError("Ya existe un cliente con ese documento.") from error

    def eliminar(self, id_cliente):
        try:
            self.database.run("DELETE FROM clientes WHERE id_cliente=?", (id_cliente,))
        except sqlite3.IntegrityError as error:
            raise ValueError("No se puede eliminar: el cliente tiene pedidos registrados.") from error
