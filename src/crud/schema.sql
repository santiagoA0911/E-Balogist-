-- ============================================================
--  E-Balogist - Esquema de base de datos (SQLite)
--
--  Espejo del DDL que ejecuta src/crud/database.py al arrancar.
--  Para levantar la base a mano:
--      sqlite3 ebalogist.db < schema.sql
--
--  Nota: la aplicacion activa las llaves foraneas con
--  PRAGMA foreign_keys = ON antes de crear las tablas. Si corres
--  este archivo por tu cuenta, ejecuta ese PRAGMA primero: SQLite
--  lo trae apagado por defecto y sin el las FOREIGN KEY no validan
--  nada. No se incluye como sentencia aqui porque dentro de un
--  script transaccional el PRAGMA se ignora en silencio.
-- ============================================================


-- ------------------------------------------------------------
--  Compras: materiales, proveedores y sus compras
-- ------------------------------------------------------------

-- Insumos que se compran para fabricar (madera, tornilleria, etc.)
CREATE TABLE IF NOT EXISTS materiales (
    id_material TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    cantidad REAL NOT NULL,
    unidad TEXT NOT NULL,
    precio REAL NOT NULL
);

-- Quien nos vende los materiales
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    tel TEXT NOT NULL,
    direccion TEXT NOT NULL,
    correo TEXT NOT NULL
);

-- Compra hecha a un proveedor
CREATE TABLE IF NOT EXISTS compras (
    id_compra TEXT PRIMARY KEY,
    fecha TEXT NOT NULL,
    valor_total REAL NOT NULL,
    estado TEXT NOT NULL,
    id_proveedor TEXT NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
);


-- ------------------------------------------------------------
--  Ventas: clientes, productos y pedidos
-- ------------------------------------------------------------

-- Cliente que hace el pedido y recibe la instalacion.
-- documento es la cedula o el NIT: UNIQUE, no se puede repetir.
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    documento TEXT NOT NULL UNIQUE,
    telefono TEXT NOT NULL,
    correo TEXT NOT NULL,
    direccion TEXT NOT NULL
);

-- Producto terminado que se vende (cocina, closet...).
-- No lleva stock: se fabrica bajo pedido; el inventario vive en materiales.
CREATE TABLE IF NOT EXISTS productos (
    id_producto TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio REAL NOT NULL
);

-- Pedido de un cliente.
-- valor_total no se digita: PedidoCRUD.recalcular_total() lo reescribe
-- como SUM(cantidad * precio_unitario) de sus detalles.
-- estado se valida contra PedidoCRUD.ESTADOS:
--   Pendiente | En produccion | En transito | Instalado | Cancelado
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

-- Linea de un pedido: que producto, cuanto y a que precio.
-- precio_unitario se copia de productos.precio al agregar el item,
-- para que el pedido conserve el precio del dia aunque el producto suba.
-- El subtotal no se guarda: es cantidad * precio_unitario.
-- ON DELETE CASCADE: borrar el pedido borra sus items.
CREATE TABLE IF NOT EXISTS detalles_pedido (
    id_detalle TEXT PRIMARY KEY,
    id_pedido TEXT NOT NULL,
    id_producto TEXT NOT NULL,
    cantidad REAL NOT NULL,
    precio_unitario REAL NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);


-- ------------------------------------------------------------
--  Pendiente: produccion, transporte, instalacion y empleado
--
--  Estas cuatro entidades existen en src/entities/ pero todavia
--  guardan sus datos en listas de Python (src/crud/crud_*.py), no
--  en esta base. Por eso no aparecen aqui como tablas.
--  Produccion e Instalacion ya guardan un id_pedido de tipo texto,
--  listo para apuntar a pedidos(id_pedido) cuando se migren.
-- ------------------------------------------------------------
