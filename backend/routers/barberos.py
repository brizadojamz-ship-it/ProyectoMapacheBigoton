from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.datos import barberos

router = APIRouter(tags=["Barberos"])

# MÓDULO DE BARBEROS
class Barbero(BaseModel):
    nombre: str


# Consultar barberos
@router.get("/barberos")
def obtener_barberos():
    return barberos


# Registrar barbero
@router.post("/barberos", status_code=201)
def registrar_barbero(barbero: Barbero):
    nuevo_barbero = {
        "id": max((b["id"] for b in barberos), default=0) + 1,
        **barbero.model_dump()
    }

    barberos.append(nuevo_barbero)
    return nuevo_barbero


# Actualizar barbero
@router.put("/barberos/{id}")
def actualizar_barbero(id: int, barbero: Barbero):
    for b in barberos:
        if b["id"] == id:
            b.update(barbero.model_dump())

            return {
                "mensaje": "Barbero actualizado correctamente",
                "barbero": b
            }

    raise HTTPException(
        status_code=404,
        detail="Barbero no encontrado"
    )


# Eliminar barbero
@router.delete("/barberos/{id}")
def eliminar_barbero(id: int):
    for b in barberos:
        if b["id"] == id:
            barberos.remove(b)

            return {"mensaje": "Barbero eliminado correctamente"}

    raise HTTPException(
        status_code=404,
        detail="Barbero no encontrado"
    )
