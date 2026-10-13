from http.client import HTTPException

from fastapi import FastAPI, HTTPException
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


# MÓDULO DE BARBEROS

barberos = [
    {"id": 1, "nombre": "Diego Ramírez"},
    {"id": 2, "nombre": "Armando Jiménez"},
    {"id": 3, "nombre": "Joaquín Torres"}
]


# Modelo de datos para barberos
class Barbero(BaseModel):
    nombre: str


# Consultar los barberos
@app.get("/barberos")
def obtener_babrberos():
    return barberos


# Registrar un nuevo barbero
@app.post("/babrberos", status_code=201)
def registrar_barbero(barbero: Barbero):
    nuevo_barbero = {
        "id": max((b["id"] for b in barberos), default=0) + 1,
        "nombre": barbero.nombre
    }

    barberos.append(nuevo_barbero)
    return nuevo_barbero


# Actualizar un barbero
@app.put("/barberos/{id}")
def actualizar_barbero(id: int, barbero: Barbero):
    for b in barberos:
        if b["id"] == id:
            b["nombre"] = barbero.nombre

            return {
                "mensaje": "Barbero actualizado correctamente",
                "barbero": b
            }

    raise HTTPException(status_code=404, detail="Barbero no encontrado")


# Eliminar un barbero
@app.delete("/barberos/{id}")
def eliminar_barbero(id: int):
    for b in barberos:
        if b["id"] == id:
            barberos.remove(b)

        return {"mensaje": "Barbero eliminado correctamente"}

    raise HTTPException(status_code=404, detail="Barbero no encontrado")
