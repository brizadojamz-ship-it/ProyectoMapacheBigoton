from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.datos import servicios

router = APIRouter(tags=["Servicios"])

# MÓDULO DE SERVICIOS
# =====================================

class Servicio(BaseModel):
    nombre: str = Field(min_length=1)
    descripcion: str
    precio: float = Field(gt=0)
    duracion: int = Field(gt=0)


# Consultar servicios
@router.get("/servicios")
def obtener_servicios():
    return servicios


# Registrar servicio
@router.post("/servicios", status_code=201)
def registrar_servicio(servicio: Servicio):
    nuevo_servicio = {
        "id": max((s["id"] for s in servicios), default=0) + 1,
        **servicio.model_dump()
    }

    servicios.append(nuevo_servicio)
    return nuevo_servicio


# Actualizar servicio
@router.put("/servicios/{id}")
def actualizar_servicio(id: int, servicio: Servicio):
    for s in servicios:
        if s["id"] == id:
            s.update(servicio.model_dump())

            return {
                "mensaje": "Servicio actualizado correctamente",
                "servicio": s
            }

    raise HTTPException(
        status_code=404,
        detail="Servicio no encontrado"
    )


# Eliminar servicio
@router.delete("/servicios/{id}")
def eliminar_servicio(id: int):
    for s in servicios:
        if s["id"] == id:
            servicios.remove(s)

            return {"mensaje": "Servicio eliminado correctamente"}

    raise HTTPException(
        status_code=404,
        detail="Servicio no encontrado"
    )


# =====================================
