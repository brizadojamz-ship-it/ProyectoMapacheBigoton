from fastapi import FastAPI
from backend.routers import clientes, barberos, servicios, citas, monitoreo

app = FastAPI(title="El Mapache Bigotón")

app.include_router(clientes.router)
app.include_router(barberos.router)
app.include_router(servicios.router)
app.include_router(citas.router)
app.include_router(monitoreo.router)

@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "Bienvenido a El Mapache Bigotón"}
