
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database.conexion import obtener_db
from database.modelos import BarberoDB

router = APIRouter(tags=["Barberos"])


class Barbero(BaseModel):
    nombre: str


# Consultar barberos
@router.get("/barberos")
def obtener_barberos(db: Session = Depends(obtener_db)):
    return db.query(BarberoDB).all()


# Registrar barbero
@router.post("/barberos", status_code=201)
def registrar_barbero(
    barbero: Barbero,
    db: Session = Depends(obtener_db)
):
    nuevo_barbero = BarberoDB(**barbero.model_dump())

    db.add(nuevo_barbero)
    db.commit()
    db.refresh(nuevo_barbero)

    return nuevo_barbero


# Actualizar barbero
@router.put("/barberos/{id}")
def actualizar_barbero(
    id: int,
    barbero: Barbero,
    db: Session = Depends(obtener_db)
):
    barbero_db = db.query(BarberoDB).filter(
        BarberoDB.id == id
    ).first()

    if not barbero_db:
        raise HTTPException(
            status_code=404,
            detail="Barbero no encontrado"
        )

    barbero_db.nombre = barbero.nombre

    db.commit()
    db.refresh(barbero_db)

    return {
        "mensaje": "Barbero actualizado correctamente",
        "barbero": barbero_db
    }


# Eliminar barbero
@router.delete("/barberos/{id}")
def eliminar_barbero(
    id: int,
    db: Session = Depends(obtener_db)
):
    barbero_db = db.query(BarberoDB).filter(
        BarberoDB.id == id
    ).first()

    if not barbero_db:
        raise HTTPException(
            status_code=404,
            detail="Barbero no encontrado"
        )

    try:
        db.delete(barbero_db)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el barbero porque tiene citas relacionadas"
        )

    return {"mensaje": "Barbero eliminado correctamente"}
