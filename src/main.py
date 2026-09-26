import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.usuarios import usuarios_router

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


app.include_router(usuarios_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


