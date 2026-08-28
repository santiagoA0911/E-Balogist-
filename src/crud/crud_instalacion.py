from src.entities.instalacion import Instalacion

class CRUDInstalacion:
    def __init__(self):
        self.instalaciones = []

    def crear(self, instalacion: Instalacion):
        self.instalaciones.append(instalacion)
        return instalacion

    def listar(self):
        return self.instalaciones

    def obtener_por_id(self, id_instalacion: int):
        for inst in self.instalaciones:
            if inst.id_instalacion == id_instalacion:
                return inst
        return None

    def actualizar(self, id_instalacion: int, nuevo_estado: str = None, nuevas_observaciones: str = None):
        instalacion = self.obtener_por_id(id_instalacion)
        if instalacion:
            if nuevo_estado:
                instalacion.estado = nuevo_estado
            if nuevas_observaciones:
                instalacion.observaciones = nuevas_observaciones
            return True
        return False

    def eliminar(self, id_instalacion: int):
        instalacion = self.obtener_por_id(id_instalacion)
        if instalacion:
            self.instalaciones.remove(instalacion)
            return True
        return False