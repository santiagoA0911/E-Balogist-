import sqlite3
from pathlib import Path


class Database:
    def __init__(self, path: Path):
        self.connection = sqlite3.connect(path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS materiales (
                id_material TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                cantidad REAL NOT NULL,
                unidad TEXT NOT NULL,
                precio REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS proveedores (
                id_proveedor TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                tel TEXT NOT NULL,
                direccion TEXT NOT NULL,
                correo TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS compras (
                id_compra TEXT PRIMARY KEY,
                fecha TEXT NOT NULL,
                valor_total REAL NOT NULL,
                estado TEXT NOT NULL,
                id_proveedor TEXT NOT NULL,
                FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
            );
            """
        )
        self.connection.commit()

    def rows(self, query, values=()):
        return self.connection.execute(query, values).fetchall()

    def run(self, query, values=()):
        self.connection.execute(query, values)
        self.connection.commit()

    def close(self):
        self.connection.close()
