from src.entities.empleado import Empleado

class CRUDEmpleado:
    def __init__(self):
        self.empleados = []

    def crear(self, empleado: Empleado):
        self.empleados.append(empleado)
        return empleado

    def listar(self):
        return self.empleados

    def obtener_por_id(self, id_empleado: int):
        for emp in self.empleados:
            if emp.id_empleado == id_empleado:
                return emp
        return None

    def actualizar(self, id_empleado: int, nuevo_cargo: str = None, nuevo_telefono: str = None, nuevo_estado: str = None):
        empleado = self.obtener_por_id(id_empleado)
        if empleado:
            if nuevo_cargo:
                empleado.cargo = nuevo_cargo
            if nuevo_telefono:
                empleado.telefono = nuevo_telefono
            if nuevo_estado:
                empleado.estado = nuevo_estado
            return True
        return False

    def eliminar(self, id_empleado: int):
        empleado = self.obtener_por_id(id_empleado)
        if empleado:
            self.empleados.remove(empleado)
            return True
        return False