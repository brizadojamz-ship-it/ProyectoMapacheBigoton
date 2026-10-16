from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.datos import clientes

router = APIRouter(tags=["Clientes"])

# MÓDULO DE CLIENTES
# =====================================

class Cliente(BaseModel):
    nombre: str
    telefono: str


# Consultar clientes
@router.get("/clientes")
def obtener_clientes():
    return clientes


# Registrar cliente
@router.post("/clientes", status_code=201)
def registrar_cliente(cliente: Cliente):
    nuevo_cliente = {
        "id": max((c["id"] for c in clientes), default=0) + 1,
        **cliente.model_dump()
    }

    clientes.append(nuevo_cliente)
    return nuevo_cliente


# Actualizar cliente
@router.put("/clientes/{id}")
def actualizar_cliente(id: int, cliente: Cliente):
    for c in clientes:
        if c["id"] == id:
            c.update(cliente.model_dump())

            return {
                "mensaje": "Cliente actualizado correctamente",
                "cliente": c
            }

    raise HTTPException(
        status_code=404,
        detail="Cliente no encontrado"
    )


# Eliminar cliente
@router.delete("/clientes/{id}")
def eliminar_cliente(id: int):
    for c in clientes:
        if c["id"] == id:
            clientes.remove(c)

            return {"mensaje": "Cliente eliminado correctamente"}

    raise HTTPException(
        status_code=404,
        detail="Cliente no encontrado"
    )


# =====================================
