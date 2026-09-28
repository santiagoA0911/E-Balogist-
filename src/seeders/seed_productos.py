"""Seeder de la tabla productos."""

from decimal import Decimal

from src.database.connection import Base, SessionLocal, engine
# Las relaciones del ORM se resuelven por nombre al configurar los mapeadores,
# asi que las cuatro entidades deben estar importadas aunque este archivo
# no las use todas. Sin esto, ejecutar el seeder suelto falla.
from src.entities.cliente import Cliente
from src.entities.detalle_pedido import DetallePedido
from src.entities.pedido import Pedido
from src.entities.producto import Producto


def sembrar(sesion):
    """Inserta los productos de prueba usando una sesion ya abierta.

    No hace commit: quien orquesta decide cuando confirmar la transaccion.
    Devuelve la lista de productos disponibles en la tabla.
    """
    if sesion.query(Producto).first():
        print("Los productos ya tienen datos, se omite el seeder.")
        return sesion.query(Producto).order_by(Producto.id).all()

    productos = [
        Producto(
            nombre="Cocina Integral en L",
            descripcion="Cocina integral en L de 3.20 m en melamina con meson en quarztone",
            categoria="Cocinas",
            precio=Decimal("5800000.00"),
        ),
        Producto(
            nombre="Closet 2 puertas",
            descripcion="Closet de 2 puertas corredizas con entrepanos y barra colgadora",
            categoria="Closets",
            precio=Decimal("2350000.00"),
        ),
        Producto(
            nombre="Mueble de bano",
            descripcion="Mueble de bano flotante de 80 cm con lavamanos y espejo",
            categoria="Banos",
            precio=Decimal("1250000.00"),
        ),
        Producto(
            nombre="Barra auxiliar",
            descripcion="Barra auxiliar de 1.50 m en madera con acabado laminado",
            categoria="Complementos",
            precio=Decimal("980000.00"),
        ),
    ]

    sesion.add_all(productos)
    sesion.flush()
    print(f"Se sembraron {len(productos)} productos.")
    return productos


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        registros = sembrar(db)
        db.commit()
        for producto in registros:
            print(producto)
    except Exception as error:
        db.rollback()
        print(f"Error al ejecutar el seeder de productos: {error}")
    finally:
        db.close()
