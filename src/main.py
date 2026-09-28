from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importación de los routers de tus entidades
from src.routers import (
    empleado_router,
    produccion_router,
    transporte_router,
    instalacion_router
)

app = FastAPI(
    title="API REST E-Balogist",
    description="API REST para la gestión logística con FastAPI, SQLAlchemy y PostgreSQL en Neon",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(empleado_router.router)
app.include_router(produccion_router.router)
app.include_router(transporte_router.router)
app.include_router(instalacion_router.router)

@app.get("/", tags=["Inicio"])
def mensaje_bienvenida():
    return {"mensaje": "Bienvenido a la API REST de E-Balogist"}