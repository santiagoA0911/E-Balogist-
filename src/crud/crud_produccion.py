from src.entities.produccion import Produccion

class CRUDProduccion:
    def __init__(self):
        self.producciones = []

    def crear(self, produccion: Produccion):
        self.producciones.append(produccion)
        return produccion

    def listar(self):
        return self.producciones

    def obtener_por_id(self, id_produccion: int):
        for p in self.producciones:
            if p.id_produccion == id_produccion:
                return p
        return None

    def actualizar(self, id_produccion: int, nuevo_estado: str = None, nueva_fecha_final: str = None):
        produccion = self.obtener_por_id(id_produccion)
        if produccion:
            if nuevo_estado:
                produccion.estado = nuevo_estado
            if nueva_fecha_final:
                produccion.fecha_final = nueva_fecha_final
            return True
        return False

    def eliminar(self, id_produccion: int):
        produccion = self.obtener_por_id(id_produccion)
        if produccion:
            self.producciones.remove(produccion)
            return True
        return False