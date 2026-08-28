class Empleado:
    def __init__(self, id_empleado: int, nombre: str, telefono: str, cargo: str, estado: str):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.telefono = telefono
        self.cargo = cargo
        self.estado = estado

    def __str__(self):
        return f"Empleado(ID: {self.id_empleado}, Nombre: {self.nombre}, Cargo: {self.cargo})"