class Produccion:
    def __init__(self, id_produccion: int, fecha_inicio: str, fecha_final: str, estado: str, tipo_trabajo: str, id_pedido: str | None = None):
        self.id_produccion = id_produccion
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final
        self.estado = estado
        self.tipo_trabajo = tipo_trabajo
        self.id_pedido = id_pedido

    def __str__(self):
        return f"Produccion(ID: {self.id_produccion}, Trabajo: {self.tipo_trabajo}, Estado: {self.estado})"