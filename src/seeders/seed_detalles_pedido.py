"""Seeder de la tabla detalles_pedido.

Depende de pedidos y productos: los consulta en vez de inventarse ids.
El precio_unitario se copia del precio del producto en ese momento y al final
se recalcula el valor_total de cada pedido afectado como SUM(cantidad * precio_unitario).
"""

from decimal import Decimal

from src.database.connection import Base, SessionLocal, engine
# Las relaciones del ORM se resuelven por nombre al configurar los mapeadores,
# asi que las cuatro entidades deben estar importadas aunque este archivo
# no las use todas. Sin esto, ejecutar el seeder suelto falla.
from src.entities.cliente import Cliente
from src.entities.detalle_pedido import DetallePedido
from src.entities.pedido import Pedido
from src.entities.producto import Producto
from src.seeders import seed_pedidos, seed_productos


def recalcular_totales(sesion, pedidos):
    """Recalcula el valor_total de cada pedido como SUM(cantidad * precio_unitario)."""
    for pedido in pedidos:
        detalles = sesion.query(DetallePedido).filter(DetallePedido.pedido_id == pedido.id).all()
        total = Decimal("0.00")
        for detalle in detalles:
            total += Decimal(detalle.cantidad) * Decimal(detalle.precio_unitario)
        pedido.valor_total = total
    sesion.flush()


def sembrar(sesion):
    """Inserta los detalles de pedido usando una sesion ya abierta.

    No hace commit: quien orquesta decide cuando confirmar la transaccion.
    Devuelve la lista de detalles disponibles en la tabla.
    """
    if sesion.query(DetallePedido).first():
        print("Los detalles_pedido ya tienen datos, se omite el seeder.")
        return sesion.query(DetallePedido).order_by(DetallePedido.id).all()

    pedidos = sesion.query(Pedido).order_by(Pedido.id).all()
    if not pedidos:
        pedidos = seed_pedidos.sembrar(sesion)

    productos = sesion.query(Producto).order_by(Producto.id).all()
    if not productos:
        productos = seed_productos.sembrar(sesion)

    if not pedidos or not productos:
        print("No hay pedidos o productos disponibles, no se pueden sembrar los detalles_pedido.")
        return []

    # (indice del pedido, indice del producto, cantidad)
    datos = [
        (0, 0, Decimal("1.00")),
        (0, 2, Decimal("2.00")),
        (1, 1, Decimal("3.00")),
        (1, 3, Decimal("1.00")),
        (2, 0, Decimal("1.00")),
        (2, 1, Decimal("2.00")),
    ]

    detalles = []
    pedidos_afectados = {}
    for indice_pedido, indice_producto, cantidad in datos:
        pedido = pedidos[indice_pedido % len(pedidos)]
        producto = productos[indice_producto % len(productos)]
        detalles.append(
            DetallePedido(
                pedido_id=pedido.id,
                producto_id=producto.id,
                cantidad=cantidad,
                precio_unitario=Decimal(producto.precio),
            )
        )
        pedidos_afectados[pedido.id] = pedido

    sesion.add_all(detalles)
    sesion.flush()

    recalcular_totales(sesion, list(pedidos_afectados.values()))

    print(f"Se sembraron {len(detalles)} detalles_pedido y se recalcularon {len(pedidos_afectados)} pedidos.")
    return detalles


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        registros = sembrar(db)
        db.commit()
        for detalle in registros:
            print(detalle)
    except Exception as error:
        db.rollback()
        print(f"Error al ejecutar el seeder de detalles_pedido: {error}")
    finally:
        db.close()
