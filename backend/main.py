from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def incio():
    return {"mensaje": "Bienvenido a El Mapache Bigotón"}


clientes = [
    {"id": 1, "nombre": "Diana Lozano", "telefono": "2311501210"},
    {"id": 2, "nombre": "Abraham Zamora", "telefono": "2223548909"}
]


@app.get("/clientes")
def obtener_clientes():
    return clientes


# Modelo para registrar clientes
class Cliente(BaseModel):
    nombre: str
    telefono: str


# Registrar un nuevo cliente
@app.post("/clientes", status_code=201)
def registrar_cliente(cliente: Cliente):
    nuevo_cliente = {
        "id": max((c["id"] for c in clientes), default=0) + 1,
        "nombre": cliente.nombre,
        "telefono": cliente.telefono
    }

    clientes.append(nuevo_cliente)
    return nuevo_cliente


# Actualizar los datos del cliente

@app.put("/clientes/{id}")
def actualizar_cliente(id: int, cliente: Cliente):
    for c in clientes:
        if c["id"] == id:
            c["nombre"] = cliente.nombre
            c["telefono"] = cliente.telefono

            return {
                "mensaje": "Cliente actualizado correctamente",
                "cliente": c
            }

    return {"mensaje": "Cliente no encontrado"}


# Eliminar un cliente por ID
@app.delete("/clientes/{id}")
def eliminar_cliente(id: int):
    for c in clientes:
        if c["id"] == id:
            clientes.remove(c)

            return {
                "mensaje": "Cliente eliminado correctamente"
            }
    return {
        "mensaje": "Error. Cliente no encontrado"
    }
