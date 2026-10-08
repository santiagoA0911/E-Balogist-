"""Seeder de la tabla pedidos.

Depende de clientes: los consulta en vez de inventarse ids.
El valor_total nace en 0 porque lo calculan los detalles del pedido.
"""

from datetime import date
from decimal import Decimal

from src.database.connection import Base, SessionLocal, engine
# Las relaciones del ORM se resuelven por nombre al configurar los mapeadores,
# asi que las cuatro entidades deben estar importadas aunque este archivo
# no las use todas. Sin esto, ejecutar el seeder suelto falla.
from src.entities.cliente import Cliente
from src.entities.detalle_pedido import DetallePedido
from src.entities.pedido import Pedido
from src.entities.producto import Producto
from src.seeders import seed_clientes


def sembrar(sesion):
    """Inserta los pedidos de prueba usando una sesion ya abierta.

    No hace commit: quien orquesta decide cuando confirmar la transaccion.
    Devuelve la lista de pedidos disponibles en la tabla.
    """
    if sesion.query(Pedido).first():
        print("Los pedidos ya tienen datos, se omite el seeder.")
        return sesion.query(Pedido).order_by(Pedido.id).all()

    clientes = sesion.query(Cliente).order_by(Cliente.id).all()
    if not clientes:
        clientes = seed_clientes.sembrar(sesion)

    if not clientes:
        print("No hay clientes disponibles, no se pueden sembrar los pedidos.")
        return []

    datos = [
        {
            "fecha": date(2026, 7, 15),
            "fecha_entrega": date(2026, 8, 20),
            "estado": Pedido.ESTADOS[3],  # Instalado
            "direccion_entrega": "Carrera 43A #18-25, Apto 802, Medellin",
        },
        {
            "fecha": date(2026, 8, 28),
            "fecha_entrega": date(2026, 9, 30),
            "estado": Pedido.ESTADOS[1],  # En produccion
            "direccion_entrega": "Calle 10 #34-12, Torre 2, Medellin",
        },
        {
            "fecha": date(2026, 9, 5),
            "fecha_entrega": date(2026, 10, 10),
            "estado": Pedido.ESTADOS[0],  # Pendiente
            "direccion_entrega": "Calle 70 #52-18, Casa 4, Itagui",
        },
    ]

    pedidos = []
    for posicion, fila in enumerate(datos):
        cliente = clientes[posicion % len(clientes)]
        pedidos.append(
            Pedido(
                cliente_id=cliente.id,
                fecha=fila["fecha"],
                fecha_entrega=fila["fecha_entrega"],
                estado=fila["estado"],
                direccion_entrega=fila["direccion_entrega"],
                valor_total=Decimal("0.00"),
            )
        )

    sesion.add_all(pedidos)
    sesion.flush()
    print(f"Se sembraron {len(pedidos)} pedidos.")
    return pedidos


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        registros = sembrar(db)
        db.commit()
        for pedido in registros:
            print(pedido)
    except Exception as error:
        db.rollback()
        print(f"Error al ejecutar el seeder de pedidos: {error}")
    finally:
        db.close()
