from datetime import date
from pathlib import Path

from crud.compra_crud import CompraCRUD
from crud.database import Database
from crud.material_crud import MaterialCRUD
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


def main():
    database = Database(DATABASE)
    acciones = (MaterialCRUD(database), ProveedorCRUD(database), CompraCRUD(database))
    try:
        while True:
            print("\n=== E-BALOGIST ===")
            print("1. Materiales\n2. Proveedores\n3. Compras\n0. Salir")
            opcion = input("Opción: ").strip()
            if opcion == "1":
                menu_materiales(acciones[0])
            elif opcion == "2":
                menu_proveedores(acciones[1])
            elif opcion == "3":
                menu_compras(acciones[2])
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
