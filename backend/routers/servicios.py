
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database.conexion import obtener_db
from database.modelos import ServicioDB

router = APIRouter(tags=["Servicios"])


class Servicio(BaseModel):
    nombre: str = Field(min_length=1)
    descripcion: str
    precio: float = Field(gt=0)
    duracion: int = Field(gt=0)


# Consultar servicios
@router.get("/servicios")
def obtener_servicios(db: Session = Depends(obtener_db)):
    return db.query(ServicioDB).all()


# Registrar servicio
@router.post("/servicios", status_code=201)
def registrar_servicio(
    servicio: Servicio,
    db: Session = Depends(obtener_db)
):
    nuevo_servicio = ServicioDB(**servicio.model_dump())

    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)

    return nuevo_servicio


# Actualizar servicio
@router.put("/servicios/{id}")
def actualizar_servicio(
    id: int,
    servicio: Servicio,
    db: Session = Depends(obtener_db)
):
    servicio_db = db.query(ServicioDB).filter(
        ServicioDB.id == id
    ).first()

    if not servicio_db:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    servicio_db.nombre = servicio.nombre
    servicio_db.descripcion = servicio.descripcion
    servicio_db.precio = servicio.precio
    servicio_db.duracion = servicio.duracion

    db.commit()
    db.refresh(servicio_db)

    return {
        "mensaje": "Servicio actualizado correctamente",
        "servicio": servicio_db
    }


# Eliminar servicio
@router.delete("/servicios/{id}")
def eliminar_servicio(
    id: int,
    db: Session = Depends(obtener_db)
):
    servicio_db = db.query(ServicioDB).filter(
        ServicioDB.id == id
    ).first()

    if not servicio_db:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    try:
        db.delete(servicio_db)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el servicio porque tiene citas relacionadas"
        )

    return {"mensaje": "Servicio eliminado correctamente"}
