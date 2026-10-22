from datetime import date, time, datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Importaciones corregidas
from database.conexion import obtener_db
from database.modelos import (
    ClienteDB,
    BarberoDB,
    ServicioDB,
    CitaDB
)

router = APIRouter(tags=["Citas"])


# MODELO DE ENTRADA
class Cita(BaseModel):
    cliente_id: int
    barbero_id: int
    servicio_id: int
    fecha: date
    hora: time


# CONSULTAR TODAS LAS CITAS
@router.get("/citas")
def obtener_citas(db: Session = Depends(obtener_db)):
    return db.query(CitaDB).all()


# VALIDAR DATOS Y DISPONIBILIDAD
def validar_cita(cita: Cita, db: Session, id_ignorar=None):

    # Verificar cliente
    cliente = db.get(ClienteDB, cita.cliente_id)

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    # Verificar barbero
    barbero = db.get(BarberoDB, cita.barbero_id)

    if barbero is None:
        raise HTTPException(
            status_code=404,
            detail="Barbero no encontrado"
        )

    # Verificar servicio
    servicio = db.get(ServicioDB, cita.servicio_id)

    if servicio is None:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    # Calcular duración de la nueva cita
    inicio_nuevo = datetime.combine(cita.fecha, cita.hora)
    fin_nuevo = inicio_nuevo + timedelta(
        minutes=servicio.duracion
    )

    # Consultar citas del mismo barbero
    citas_existentes = db.query(CitaDB).filter(
        CitaDB.barbero_id == cita.barbero_id
    ).all()

    for existente in citas_existentes:

        # Ignorar la cita que se está actualizando
        if existente.id == id_ignorar:
            continue

        inicio_existente = datetime.combine(
            existente.fecha,
            existente.hora
        )

        servicio_existente = db.get(
            ServicioDB,
            existente.servicio_id
        )

        if servicio_existente is None:
            raise HTTPException(
                status_code=409,
                detail="Una cita existente tiene un servicio no disponible"
            )

        fin_existente = inicio_existente + timedelta(
            minutes=servicio_existente.duracion
        )

        # Evitar horarios empalmados
        if inicio_nuevo < fin_existente and fin_nuevo > inicio_existente:
            raise HTTPException(
                status_code=409,
                detail="El barbero ya tiene una cita en ese horario"
            )


# REGISTRAR CITA
@router.post("/citas", status_code=201)
def registrar_cita(
    cita: Cita,
    db: Session = Depends(obtener_db)
):

    validar_cita(cita, db)

    nueva_cita = CitaDB(**cita.model_dump())

    db.add(nueva_cita)

    try:
        db.commit()
        db.refresh(nueva_cita)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se pudo registrar la cita"
        )

    return nueva_cita


# ELIMINAR CITA
@router.delete("/citas/{id}")
def eliminar_cita(
    id: int,
    db: Session = Depends(obtener_db)
):

    cita_db = db.get(CitaDB, id)

    if cita_db is None:
        raise HTTPException(
            status_code=404,
            detail="Cita no encontrada"
        )

    db.delete(cita_db)
    db.commit()

    return {
        "mensaje": "Cita eliminada correctamente"
    }


# ACTUALIZAR CITA
@router.put("/citas/{id}")
def actualizar_cita(
    id: int,
    cita: Cita,
    db: Session = Depends(obtener_db)
):

    cita_actual = db.get(CitaDB, id)

    if cita_actual is None:
        raise HTTPException(
            status_code=404,
            detail="Cita no encontrada"
        )

    validar_cita(cita, db, id_ignorar=id)

    cita_actual.cliente_id = cita.cliente_id
    cita_actual.barbero_id = cita.barbero_id
    cita_actual.servicio_id = cita.servicio_id
    cita_actual.fecha = cita.fecha
    cita_actual.hora = cita.hora

    try:
        db.commit()
        db.refresh(cita_actual)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se pudo actualizar la cita"
        )

    return {
        "mensaje": "Cita actualizada correctamente",
        "cita": cita_actual
    }