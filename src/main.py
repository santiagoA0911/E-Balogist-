
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers.material import material_router
from routers.compra import compra_router
from routers.proveedor import proveedor_router
from routers.clientes import clientes_router
from routers.productos import productos_router
from routers.pedidos import pedido_router
from routers.detalles_pedido import detalles_pedido_router

import os
from dotenv import load_dotenv

# --- Tablas ORM (entidades de SQLAlchemy) ---
from src.database.connection import Base, engine
# Hay que importar todas las entidades para que SQLAlchemy las registre y cree sus tablas
from src.entities import cliente, producto, pedido, detalle_pedido  # noqa: F401
from src.entities import empleado, instalacion, produccion, transporte  # noqa: F401

try:
    Base.metadata.create_all(bind=engine)
except Exception as error:
    print(f"⚠️ No se pudieron crear las tablas ORM en Neon: {error}")
# Esto fuerza a leer el .env que está en la carpeta padre (la raíz)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))


# Creamos la aplicación FastAPI.
app = FastAPI(
    title="API Banco — Programacion de software 2026-2",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def raiz():
    return {"mensaje": "API en marcha"}

app.include_router(material_router)
app.include_router(compra_router)
app.include_router(proveedor_router)
app.include_router(pedido_router)
app.include_router(detalles_pedido_router)
app.include_router(clientes_router)  # Clientes
app.include_router(productos_router)  # Productos


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
