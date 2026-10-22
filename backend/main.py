from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importación directa desde routers (evita el error 'No module named backend')
from routers import clientes, barberos, servicios, citas, monitoreo

app = FastAPI(title="El Mapache Bigotón")

# Configuración de CORS adaptada para tu frontend en Live Server/HTML local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
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
