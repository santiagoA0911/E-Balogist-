from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.clientes import router as clientes_router
from src.routers.productos import router as productos_router
from src.routers.pedidos import router as pedidos_router
from src.routers.detalles_pedido import router as detalles_pedido_router

app = FastAPI(
    title="E-Balogist API",
    description="API REST para la gestión de E-Balogist",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes_router)
app.include_router(productos_router)
app.include_router(pedidos_router)
app.include_router(detalles_pedido_router)


@app.get("/")
def inicio():
    return {"mensaje": "E-Balogist API funcionando"}



