import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import messagebox, ttk

from crud.compra_crud import CompraCRUD
from crud.database import Database
from crud.material_crud import MaterialCRUD
from crud.proveedor_crud import ProveedorCRUD


DATABASE = Path(__file__).with_name("ebalogist.db")


def required(values):
    if any(not value for value in values):
        raise ValueError("Todos los campos son obligatorios.")
    return tuple(values)


def decimal(value, label):
    try:
        number = float(value)
    except ValueError as error:
        raise ValueError(f"{label} debe ser un número.") from error
    if number < 0:
        raise ValueError(f"{label} no puede ser negativo.")
    return number


class CrudView:
    def __init__(self, notebook, title, fields, columns, actions, parser):
        self.actions = actions
        self.fields = fields
        self.columns = columns
        self.parser = parser
        self.selected_id = None
        self.variables = {name: tk.StringVar() for name, _ in fields}

        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=title)
        form = ttk.LabelFrame(frame, text=f"Datos de {title.lower()}", padding=8)
        form.pack(fill="x")
        for index, (name, label) in enumerate(fields):
            row, column = divmod(index, 2)
            ttk.Label(form, text=label).grid(row=row, column=column * 2, sticky="w", padx=5, pady=4)
            ttk.Entry(form, textvariable=self.variables[name], width=34).grid(row=row, column=column * 2 + 1, sticky="ew", padx=5, pady=4)
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", pady=8)
        ttk.Button(buttons, text="Nuevo", command=self.clear).pack(side="left", padx=3)
        ttk.Button(buttons, text="Guardar", command=self.save).pack(side="left", padx=3)
        ttk.Button(buttons, text="Eliminar", command=self.delete).pack(side="left", padx=3)

        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        for column in columns:
            self.tree.heading(column, text=column.replace("_", " ").title())
            self.tree.column(column, width=145)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.select)
        self.refresh()

    def clear(self):
        self.selected_id = None
        for variable in self.variables.values():
            variable.set("")
        if "fecha" in self.variables:
            self.variables["fecha"].set(date.today().isoformat())
        print("Formulario limpiado")

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.actions.listar():
            self.tree.insert("", "end", iid=row[0], values=row)

    def select(self, _event=None):
        selection = self.tree.selection()
        if not selection:
            return
        self.selected_id = selection[0]
        row = self.actions.obtener(self.selected_id)
        for variable, value in zip(self.variables.values(), row):
            variable.set(value)
        print(f"Registro consultado: {self.selected_id}")

    def save(self):
        try:
            values = self.parser([self.variables[name].get().strip() for name, _ in self.fields])
            if self.selected_id:
                self.actions.actualizar(self.selected_id, *values)
                print(f"Registro actualizado: {self.selected_id}")
            else:
                identifier = self.actions.crear(*values)
                print(f"Registro creado: {identifier}")
            self.clear()
            self.refresh()
        except (ValueError, TypeError) as error:
            messagebox.showerror("No se pudo guardar", str(error))

    def delete(self):
        if not self.selected_id:
            messagebox.showinfo("Eliminar", "Selecciona un registro primero.")
            return
        if messagebox.askyesno("Eliminar", "¿Eliminar el registro seleccionado?"):
            try:
                self.actions.eliminar(self.selected_id)
                print(f"Registro eliminado: {self.selected_id}")
                self.clear()
                self.refresh()
            except Exception as error:
                messagebox.showerror("No se pudo eliminar", str(error))


def build_app():
    database = Database(DATABASE)
    material_actions = MaterialCRUD(database)
    proveedor_actions = ProveedorCRUD(database)
    compra_actions = CompraCRUD(database)

    window = tk.Tk()
    window.title("E-Balogist - Gestión de compras")
    window.geometry("1050x600")
    notebook = ttk.Notebook(window)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    CrudView(
        notebook,
        "Materiales",
        [("nombre", "Nombre"), ("tipo", "Tipo"), ("cantidad", "Cantidad"), ("unidad", "Unidad"), ("precio", "Precio")],
        material_actions.columns,
        material_actions,
        lambda values: (required(values[:2])[0], required(values[:2])[1], decimal(values[2], "Cantidad"), required(values[3:5])[0], decimal(values[4], "Precio")),
    )
    CrudView(
        notebook,
        "Proveedores",
        [("nombre", "Nombre"), ("tel", "Teléfono"), ("direccion", "Dirección"), ("correo", "Correo")],
        proveedor_actions.columns,
        proveedor_actions,
        required,
    )
    CrudView(
        notebook,
        "Compras",
        [("fecha", "Fecha (AAAA-MM-DD)"), ("valor_total", "Valor total"), ("estado", "Estado"), ("id_proveedor", "ID proveedor")],
        compra_actions.columns,
        compra_actions,
        lambda values: (required(values)[0], decimal(values[1], "Valor total"), required(values)[2], required(values)[3]),
    )

    window.protocol("WM_DELETE_WINDOW", lambda: (database.close(), window.destroy()))
    window.mainloop()


if __name__ == "__main__":
    build_app()
