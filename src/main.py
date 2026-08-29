from datetime import date
from pathlib import Path

from crud.cliente_crud import ClienteCRUD
from crud.compra_crud import CompraCRUD
from crud.database import Database
from crud.detalle_pedido_crud import DetallePedidoCRUD
from crud.material_crud import MaterialCRUD
from crud.pedido_crud import PedidoCRUD
from crud.producto_crud import ProductoCRUD
from crud.proveedor_crud import ProveedorCRUD


DATABASE = Path(__file__).with_name("ebalogist.db")


def obligatorio(mensaje, actual=None):
    while True:
        sugerencia = f" [{actual}]" if actual is not None else ""
        valor = input(f"{mensaje}{sugerencia}: ").strip()
        if valor:
            return valor
        if actual is not None:
            return actual
        print("El valor es obligatorio.")


def decimal(mensaje, actual=None):
    while True:
        sugerencia = f" [{actual}]" if actual is not None else ""
        valor = input(f"{mensaje}{sugerencia}: ").strip()
        if not valor and actual is not None:
            return actual
        try:
            numero = float(valor)
            if numero < 0:
                raise ValueError
            return numero
        except ValueError:
            print("Ingresa un número válido que no sea negativo.")


def mostrar(columnas, filas):
    if not filas:
        print("No hay registros.")
        return
    print("\n" + " | ".join(columnas))
    print("-" * 120)
    for fila in filas:
        print(" | ".join(str(valor) for valor in fila))


def pedir_id(acciones):
    filas = acciones.listar()
    mostrar(acciones.columns, filas)
    if not filas:
        return None
    return input("ID del registro: ").strip()


def elegir(acciones, mensaje):
    filas = acciones.listar()
    mostrar(acciones.columns, filas)
    if not filas:
        print("No hay registros para elegir. Crea uno primero.")
        return None
    return input(f"{mensaje}: ").strip()


def menu_materiales(acciones):
    while True:
        print("\n--- MATERIALES ---")
        print("1. Listar\n2. Crear\n3. Actualizar\n4. Eliminar\n0. Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                mostrar(acciones.columns, acciones.listar())
            elif opcion == "2":
                identifier = acciones.crear(obligatorio("Nombre"), obligatorio("Tipo"), decimal("Cantidad"), obligatorio("Unidad"), decimal("Precio"))
                print(f"Material creado: {identifier}")
            elif opcion == "3":
                identifier = pedir_id(acciones)
                if identifier:
                    actual = acciones.obtener(identifier)
                    acciones.actualizar(identifier, obligatorio("Nombre", actual[0]), obligatorio("Tipo", actual[1]), decimal("Cantidad", actual[2]), obligatorio("Unidad", actual[3]), decimal("Precio", actual[4]))
                    print("Material actualizado.")
            elif opcion == "4":
                identifier = pedir_id(acciones)
                if identifier:
                    acciones.eliminar(identifier)
                    print("Material eliminado.")
            elif opcion == "0":
                return
            else:
                print("Opción no válida.")
        except (IndexError, ValueError) as error:
            print(f"No se pudo completar la acción: {error}")


def menu_proveedores(acciones):
    while True:
        print("\n--- PROVEEDORES ---")
        print("1. Listar\n2. Crear\n3. Actualizar\n4. Eliminar\n0. Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                mostrar(acciones.columns, acciones.listar())
            elif opcion == "2":
                identifier = acciones.crear(obligatorio("Nombre"), obligatorio("Teléfono"), obligatorio("Dirección"), obligatorio("Correo"))
                print(f"Proveedor creado: {identifier}")
            elif opcion == "3":
                identifier = pedir_id(acciones)
                if identifier:
                    actual = acciones.obtener(identifier)
                    acciones.actualizar(identifier, obligatorio("Nombre", actual[0]), obligatorio("Teléfono", actual[1]), obligatorio("Dirección", actual[2]), obligatorio("Correo", actual[3]))
                    print("Proveedor actualizado.")
            elif opcion == "4":
                identifier = pedir_id(acciones)
                if identifier:
                    acciones.eliminar(identifier)
                    print("Proveedor eliminado.")
            elif opcion == "0":
                return
            else:
                print("Opción no válida.")
        except (IndexError, ValueError) as error:
            print(f"No se pudo completar la acción: {error}")


def menu_compras(acciones):
    while True:
        print("\n--- COMPRAS ---")
        print("1. Listar\n2. Crear\n3. Actualizar\n4. Eliminar\n0. Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                mostrar(acciones.columns, acciones.listar())
            elif opcion == "2":
                identifier = acciones.crear(obligatorio("Fecha", date.today().isoformat()), decimal("Valor total"), obligatorio("Estado", "Pendiente"), obligatorio("ID del proveedor"))
                print(f"Compra creada: {identifier}")
            elif opcion == "3":
                identifier = pedir_id(acciones)
                if identifier:
                    actual = acciones.obtener(identifier)
                    acciones.actualizar(identifier, obligatorio("Fecha", actual[0]), decimal("Valor total", actual[1]), obligatorio("Estado", actual[2]), obligatorio("ID del proveedor", actual[3]))
                    print("Compra actualizada.")
            elif opcion == "4":
                identifier = pedir_id(acciones)
                if identifier:
                    acciones.eliminar(identifier)
                    print("Compra eliminada.")
            elif opcion == "0":
                return
            else:
                print("Opción no válida.")
        except (IndexError, ValueError) as error:
            print(f"No se pudo completar la acción: {error}")


def menu_clientes(acciones):
    while True:
        print("\n--- CLIENTES ---")
        print("1. Listar\n2. Crear\n3. Actualizar\n4. Eliminar\n0. Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                mostrar(acciones.columns, acciones.listar())
            elif opcion == "2":
                identifier = acciones.crear(obligatorio("Nombre"), obligatorio("Documento"), obligatorio("Teléfono"), obligatorio("Correo"), obligatorio("Dirección"))
                print(f"Cliente creado: {identifier}")
            elif opcion == "3":
                identifier = pedir_id(acciones)
                if identifier:
                    actual = acciones.obtener(identifier)
                    acciones.actualizar(identifier, obligatorio("Nombre", actual[0]), obligatorio("Documento", actual[1]), obligatorio("Teléfono", actual[2]), obligatorio("Correo", actual[3]), obligatorio("Dirección", actual[4]))
                    print("Cliente actualizado.")
            elif opcion == "4":
                identifier = pedir_id(acciones)
                if identifier:
                    acciones.eliminar(identifier)
                    print("Cliente eliminado.")
            elif opcion == "0":
                return
            else:
                print("Opción no válida.")
        except (IndexError, ValueError) as error:
            print(f"No se pudo completar la acción: {error}")


def menu_productos(acciones):
    while True:
        print("\n--- PRODUCTOS ---")
        print("1. Listar\n2. Crear\n3. Actualizar\n4. Eliminar\n0. Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                mostrar(acciones.columns, acciones.listar())
            elif opcion == "2":
                identifier = acciones.crear(obligatorio("Nombre"), obligatorio("Descripción"), obligatorio("Categoría"), decimal("Precio"))
                print(f"Producto creado: {identifier}")
            elif opcion == "3":
                identifier = pedir_id(acciones)
                if identifier:
                    actual = acciones.obtener(identifier)
                    acciones.actualizar(identifier, obligatorio("Nombre", actual[0]), obligatorio("Descripción", actual[1]), obligatorio("Categoría", actual[2]), decimal("Precio", actual[3]))
                    print("Producto actualizado.")
            elif opcion == "4":
                identifier = pedir_id(acciones)
                if identifier:
                    acciones.eliminar(identifier)
                    print("Producto eliminado.")
            elif opcion == "0":
                return
            else:
                print("Opción no válida.")
        except (IndexError, ValueError) as error:
            print(f"No se pudo completar la acción: {error}")


def menu_pedidos(acciones, clientes, productos, detalles):
    while True:
        print("\n--- PEDIDOS ---")
        print("1. Listar\n2. Crear\n3. Actualizar\n4. Eliminar")
        print("5. Ver ítems de un pedido\n6. Agregar ítem a un pedido\n7. Quitar ítem de un pedido\n0. Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                mostrar(acciones.columns, acciones.listar())
            elif opcion == "2":
                id_cliente = elegir(clientes, "ID del cliente")
                if id_cliente:
                    print(f"Estados: {', '.join(acciones.ESTADOS)}")
                    identifier = acciones.crear(id_cliente, obligatorio("Fecha", date.today().isoformat()), obligatorio("Fecha de entrega"), obligatorio("Estado", "Pendiente"), obligatorio("Dirección de entrega"))
                    print(f"Pedido creado: {identifier}. Agrega sus ítems con la opción 6.")
            elif opcion == "3":
                identifier = pedir_id(acciones)
                if identifier:
                    actual = acciones.obtener(identifier)
                    print(f"Estados: {', '.join(acciones.ESTADOS)}")
                    acciones.actualizar(identifier, obligatorio("ID del cliente", actual[0]), obligatorio("Fecha", actual[1]), obligatorio("Fecha de entrega", actual[2]), obligatorio("Estado", actual[3]), obligatorio("Dirección de entrega", actual[4]))
                    print("Pedido actualizado.")
            elif opcion == "4":
                identifier = pedir_id(acciones)
                if identifier:
                    acciones.eliminar(identifier)
                    print("Pedido eliminado junto con sus ítems.")
            elif opcion == "5":
                identifier = pedir_id(acciones)
                if identifier:
                    mostrar(detalles.columns, detalles.listar_por_pedido(identifier))
            elif opcion == "6":
                identifier = pedir_id(acciones)
                if identifier:
                    id_producto = elegir(productos, "ID del producto")
                    if id_producto:
                        detalles.crear(identifier, id_producto, decimal("Cantidad"))
                        print(f"Ítem agregado. Nuevo total del pedido: {acciones.obtener(identifier)[5]}")
            elif opcion == "7":
                identifier = pedir_id(acciones)
                if identifier:
                    filas = detalles.listar_por_pedido(identifier)
                    mostrar(detalles.columns, filas)
                    if filas:
                        detalles.eliminar(input("ID del ítem: ").strip())
                        print(f"Ítem eliminado. Nuevo total del pedido: {acciones.obtener(identifier)[5]}")
            elif opcion == "0":
                return
            else:
                print("Opción no válida.")
        except (IndexError, ValueError) as error:
            print(f"No se pudo completar la acción: {error}")


def main():
    database = Database(DATABASE)
    materiales = MaterialCRUD(database)
    proveedores = ProveedorCRUD(database)
    compras = CompraCRUD(database)
    clientes = ClienteCRUD(database)
    productos = ProductoCRUD(database)
    pedidos = PedidoCRUD(database)
    detalles = DetallePedidoCRUD(database, pedidos)
    try:
        while True:
            print("\n=== E-BALOGIST ===")
            print("1. Materiales\n2. Proveedores\n3. Compras\n4. Clientes\n5. Productos\n6. Pedidos\n0. Salir")
            opcion = input("Opción: ").strip()
            if opcion == "1":
                menu_materiales(materiales)
            elif opcion == "2":
                menu_proveedores(proveedores)
            elif opcion == "3":
                menu_compras(compras)
            elif opcion == "4":
                menu_clientes(clientes)
            elif opcion == "5":
                menu_productos(productos)
            elif opcion == "6":
                menu_pedidos(pedidos, clientes, productos, detalles)
            elif opcion == "0":
                print("Programa finalizado.")
                return
            else:
                print("Opción no válida.")
    except KeyboardInterrupt:
        print("\nPrograma finalizado.")
    finally:
        database.close()


if __name__ == "__main__":
    main()
