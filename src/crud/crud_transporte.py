from src.entities.transporte import Transporte

class CRUDTransporte:
    def __init__(self):
        self.transportes = []

    def crear(self, transporte: Transporte):
        self.transportes.append(transporte)
        return transporte

    def listar(self):
        return self.transportes

    def obtener_por_id(self, id_transporte: int):
        for t in self.transportes:
            if t.id_transporte == id_transporte:
                return t
        return None

    def actualizar(self, id_transporte: int, nuevo_estado: str = None, nuevo_destino: str = None):
        transporte = self.obtener_por_id(id_transporte)
        if transporte:
            if nuevo_estado:
                transporte.estado = nuevo_estado
            if nuevo_destino:
                transporte.destino = nuevo_destino
            return True
        return False

    def eliminar(self, id_transporte: int):
        transporte = self.obtener_por_id(id_transporte)
        if transporte:
            self.transportes.remove(transporte)
            return True
        return False