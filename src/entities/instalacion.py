class Instalacion:
    def __init__(self, id_instalacion: int, fecha: str, direccion: str, estado: str, observaciones: str, id_pedido: str | None = None):
        self.id_instalacion = id_instalacion
        self.fecha = fecha
        self.direccion = direccion
        self.estado = estado
        self.observaciones = observaciones
        self.id_pedido = id_pedido

    def __str__(self):
        return f"Instalacion(ID: {self.id_instalacion}, Direccion: {self.direccion}, Estado: {self.estado})"