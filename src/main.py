

from api.material import material_router
from api.compra import compra_router
from api.proveedor import proveedor_router

app = FastAPI(
    title="API Banco — Programacion de software 2026-2",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en desarrollo; luego el origen real del frontend
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

#si el archivo que se ejecuta es main.py, entonces ejecuta uvicorn para levantar el servidor
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)


