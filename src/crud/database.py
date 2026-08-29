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
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                documento TEXT NOT NULL UNIQUE,
                telefono TEXT NOT NULL,
                correo TEXT NOT NULL,
                direccion TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS productos (
                id_producto TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS pedidos (
                id_pedido TEXT PRIMARY KEY,
                id_cliente TEXT NOT NULL,
                fecha TEXT NOT NULL,
                fecha_entrega TEXT NOT NULL,
                estado TEXT NOT NULL,
                direccion_entrega TEXT NOT NULL,
                valor_total REAL NOT NULL DEFAULT 0,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
            );
            CREATE TABLE IF NOT EXISTS detalles_pedido (
                id_detalle TEXT PRIMARY KEY,
                id_pedido TEXT NOT NULL,
                id_producto TEXT NOT NULL,
                cantidad REAL NOT NULL,
                precio_unitario REAL NOT NULL,
                FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
                FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
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
