class Transporte:
    def __init__(self, id_transporte: int, fecha: str, origen: str, destino: str, tipo_transporte: str, estado: str):
        self.id_transporte = id_transporte
        self.fecha = fecha
        self.origen = origen
        self.destino = destino
        self.tipo_transporte = tipo_transporte
        self.estado = estado

    def __str__(self):
        return f"Transporte(ID: {self.id_transporte}, Origen: {self.origen}, Destino: {self.destino}, Estado: {self.estado})"