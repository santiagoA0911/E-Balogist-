"""Seeder de la tabla clientes."""

from src.database.connection import Base, SessionLocal, engine
# Las relaciones del ORM se resuelven por nombre al configurar los mapeadores,
# asi que las cuatro entidades deben estar importadas aunque este archivo
# no las use todas. Sin esto, ejecutar el seeder suelto falla.
from src.entities.cliente import Cliente
from src.entities.detalle_pedido import DetallePedido
from src.entities.pedido import Pedido
from src.entities.producto import Producto


def sembrar(sesion):
    """Inserta los clientes de prueba usando una sesion ya abierta.

    No hace commit: quien orquesta decide cuando confirmar la transaccion.
    Devuelve la lista de clientes disponibles en la tabla.
    """
    if sesion.query(Cliente).first():
        print("Los clientes ya tienen datos, se omite el seeder.")
        return sesion.query(Cliente).order_by(Cliente.id).all()

    clientes = [
        Cliente(
            nombre="Luz Marina Ospina",
            documento="43567890",
            telefono="3104567890",
            correo="luz.ospina@correo.com",
            direccion="Carrera 43A #18-25, Medellin",
        ),
        Cliente(
            nombre="Constructora El Poblado S.A.S.",
            documento="900456789-1",
            telefono="6042345678",
            correo="compras@constructoraelpoblado.com",
            direccion="Calle 10 #34-12, Medellin",
        ),
        Cliente(
            nombre="Jorge Andres Cardona",
            documento="71234567",
            telefono="3157788990",
            correo="jorge.cardona@correo.com",
            direccion="Calle 70 #52-18, Itagui",
        ),
    ]

    sesion.add_all(clientes)
    sesion.flush()
    print(f"Se sembraron {len(clientes)} clientes.")
    return clientes


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        registros = sembrar(db)
        db.commit()
        for cliente in registros:
            print(cliente)
    except Exception as error:
        db.rollback()
        print(f"Error al ejecutar el seeder de clientes: {error}")
    finally:
        db.close()
