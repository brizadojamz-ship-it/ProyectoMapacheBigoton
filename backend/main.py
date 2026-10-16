
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import clientes, barberos, servicios, citas, monitoreo

app = FastAPI(title="El Mapache Bigotón")

# Configuración de CORS para conectar con el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers del backend
app.include_router(clientes.router)
app.include_router(barberos.router)
app.include_router(servicios.router)
app.include_router(citas.router)
app.include_router(monitoreo.router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "Bienvenido a El Mapache Bigotón"}
