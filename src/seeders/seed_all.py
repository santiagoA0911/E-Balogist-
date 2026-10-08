from src.database.connection import SessionLocal, engine, Base
from src.entities.empleado import Empleado
from src.entities.produccion import Produccion
from src.entities.transporte import Transporte
from src.entities.instalacion import Instalacion
from src.seeders import seed_clientes, seed_detalles_pedido, seed_pedidos, seed_productos

def sembrar_entidades_base(db):
    """Seeders originales: empleados, producción, transporte e instalación."""
    # Verificar si ya existen datos para evitar duplicados en pruebas
    if db.query(Empleado).first():
        print("Los seeders ya fueron ejecutados anteriormente.")
        return

    # 2. Insertar Empleados de prueba
    emp1 = Empleado(nombre="Carlos Pérez", cargo="Técnico de Producción", estado="Activo")
    emp2 = Empleado(nombre="María Rodríguez", cargo="Conductora Logística", estado="Activo")
    db.add_all([emp1, emp2])
    db.commit()

    # 3. Insertar Producción ligada al Empleado 1
    prod1 = Produccion(trabajo="Corte de Estructuras Metálicas", estado="Completado", empleado_id=emp1.id)
    db.add(prod1)
    db.commit()

    # 4. Insertar Transporte ligado a la Producción 1
    trans1 = Transporte(origen="Planta Principal", destino="Bodega Norte", estado="En tránsito", produccion_id=prod1.id)
    db.add(trans1)
    db.commit()

    # 5. Insertar Instalación ligada al Transporte 1
    inst1 = Instalacion(direccion="Calle 45 #12-34", estado="En proceso", transporte_id=trans1.id)
    db.add(inst1)
    db.commit()

def run_seeders():
    # 1. Crear automáticamente las tablas en Neon PostgreSQL si no existen
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Los seeders originales se detienen solos si ya hay empleados,
        # pero eso no debe impedir sembrar las tablas nuevas.
        sembrar_entidades_base(db)

        # 6. Un seeder por tabla: clientes, productos, pedidos y detalles de pedido
        seed_clientes.sembrar(db)
        seed_productos.sembrar(db)
        seed_pedidos.sembrar(db)
        seed_detalles_pedido.sembrar(db)
        db.commit()

        print("¡Seeders ejecutados con éxito y datos insertados en Neon PostgreSQL!")
    except Exception as e:
        db.rollback()
        print(f"Error al ejecutar los seeders: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_seeders()
