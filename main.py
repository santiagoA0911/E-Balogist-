from src.entities.produccion import Produccion
from src.entities.transporte import Transporte
from src.entities.instalacion import Instalacion
from src.entities.empleado import Empleado

from src.crud.crud_produccion import CRUDProduccion
from src.crud.crud_transporte import CRUDTransporte
from src.crud.crud_instalacion import CRUDInstalacion
from src.crud.crud_empleado import CRUDEmpleado


def probar_modulo_produccion_logistica():
    print("=" * 50)
    print(" PRUEBAS DE MÓDULOS: PRODUCCIÓN Y LOGÍSTICA")
    print("=" * 50)

    # 1. Instanciar CRUDs
    crud_emp = CRUDEmpleado()
    crud_prod = CRUDProduccion()
    crud_trans = CRUDTransporte()
    crud_inst = CRUDInstalacion()

    # --- CREATE ---
    print("\n1. [CREATE] Creando registros...")
    emp1 = Empleado(1, "Carlos Pérez", "3001234567", "Instalador", "Activo")
    prod1 = Produccion(1, "2026-08-27", "2026-08-30", "En fabricación", "Cocina Integral", id_pedido=101)
    trans1 = Transporte(1, "2026-08-28", "Taller Central", "Calle 10 #45-12", "Camión de carga", "En tránsito")
    inst1 = Instalacion(1, "2026-08-29", "Calle 10 #45-12", "Pendiente", "Requiere nivelación de pared", id_pedido=101)

    crud_emp.crear(emp1)
    crud_prod.crear(prod1)
    crud_trans.crear(trans1)
    crud_inst.crear(inst1)

    # --- READ ---
    print("\n2. [READ] Consultando registros creados:")
    print(" Empleado registrado:", crud_emp.obtener_por_id(1))
    print(" Producción iniciada:", crud_prod.obtener_por_id(1))
    print(" Transporte programado:", crud_trans.obtener_por_id(1))
    print(" Instalación agendada:", crud_inst.obtener_por_id(1))

    # --- UPDATE ---
    print("\n3. [UPDATE] Actualizando cargo de empleado y estado de producción...")
    crud_emp.actualizar(1, nuevo_cargo="Jefe de Instalaciones")
    crud_prod.actualizar(1, nuevo_estado="Finalizado")

    print(" Empleado modificado:", crud_emp.obtener_por_id(1))
    print(" Producción modificada:", crud_prod.obtener_por_id(1))

    # --- DELETE ---
    print("\n4. [DELETE] Eliminando el registro de transporte...")
    crud_trans.eliminar(1)
    print(" Total transportes activos:", len(crud_trans.listar()))


def main():
    probar_modulo_produccion_logistica()


if __name__ == "__main__":
    main()