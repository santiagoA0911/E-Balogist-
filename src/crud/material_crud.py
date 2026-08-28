from uuid import uuid4


class MaterialCRUD:
    columns = ("id_material", "nombre", "tipo", "cantidad", "unidad", "precio")

    def __init__(self, database):
        self.database = database

    def listar(self):
        return self.database.rows("SELECT id_material, nombre, tipo, cantidad, unidad, precio FROM materiales")

    def obtener(self, id_material):
        return self.database.rows(
            "SELECT nombre, tipo, cantidad, unidad, precio FROM materiales WHERE id_material = ?",
            (id_material,),
        )[0]

    def crear(self, nombre, tipo, cantidad, unidad, precio):
        id_material = str(uuid4())
        self.database.run(
            "INSERT INTO materiales VALUES (?, ?, ?, ?, ?, ?)",
            (id_material, nombre, tipo, cantidad, unidad, precio),
        )
        return id_material

    def actualizar(self, id_material, nombre, tipo, cantidad, unidad, precio):
        self.database.run(
            "UPDATE materiales SET nombre=?, tipo=?, cantidad=?, unidad=?, precio=? WHERE id_material=?",
            (nombre, tipo, cantidad, unidad, precio, id_material),
        )

    def eliminar(self, id_material):
        self.database.run("DELETE FROM materiales WHERE id_material=?", (id_material,))
