from datetime import date, time, datetime, timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.datos import clientes, barberos, servicios, citas

router = APIRouter(tags=["Citas"])

# MÓDULO DE CITAS
# =====================================

class Cita(BaseModel):
    cliente_id: int
    barbero_id: int
    servicio_id: int
    fecha: date
    hora: time


# Consultar todas las citas
@router.get("/citas")
def obtener_citas():
    return citas


# Registrar una cita
@router.post("/citas", status_code=201)
def registrar_cita(cita: Cita):

    # Verificar que el cliente exista
    if not any(c["id"] == cita.cliente_id for c in clientes):
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    # Verificar que el barbero exista
    if not any(b["id"] == cita.barbero_id for b in barberos):
        raise HTTPException(
            status_code=404,
            detail="Barbero no encontrado"
        )

    # Buscar el servicio solicitado
    servicio = next(
        (s for s in servicios if s["id"] == cita.servicio_id),
        None
    )

    if servicio is None:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    # Calcular el horario de la nueva cita
    inicio_nuevo = datetime.combine(cita.fecha, cita.hora)

    fin_nuevo = inicio_nuevo + timedelta(
        minutes=servicio["duracion"]
    )

    # Revisar si el barbero tiene otra cita
    for existente in citas:

        if existente["barbero_id"] == cita.barbero_id:

            inicio_existente = datetime.combine(
                date.fromisoformat(existente["fecha"]),
                time.fromisoformat(existente["hora"])
            )

            servicio_existente = next(
                (
                    s for s in servicios
                    if s["id"] == existente["servicio_id"]
                ),
                None
            )

            if servicio_existente is None:
                raise HTTPException(
                    status_code=409,
                    detail="Una cita existente tiene un servicio no disponible"
                )

            fin_existente = inicio_existente + timedelta(
                minutes=servicio_existente["duracion"]
            )

            # Verificar si los horarios se empalman
            if inicio_nuevo < fin_existente and fin_nuevo > inicio_existente:
                raise HTTPException(
                    status_code=409,
                    detail="El barbero ya tiene una cita en ese horario"
                )

    # Guardar la nueva cita
    nueva_cita = {
        "id": max((c["id"] for c in citas), default=0) + 1,
        **cita.model_dump(mode="json")
    }

    citas.append(nueva_cita)

    return nueva_cita


#Eliminar
@router.delete("/citas/{id}")
def eliminar_cita(id: int):

    for c in citas:
        if c["id"] == id:
            citas.remove(c)

            return {
                "mensaje": "Cita eliminada correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Cita no encontrada"
    )

# ACTUALIZAR CITAS


@router.put("/citas/{id}")
def actualizar_cita(id: int, cita: Cita):

    # Buscar la cita que queremos modificar
    cita_actual = next(
        (c for c in citas if c["id"] == id),
        None
    )

    if cita_actual is None:
        raise HTTPException(
            status_code=404,
            detail="Cita no encontrada"
        )

    # Comprobar que el cliente exista
    if not any(c["id"] == cita.cliente_id for c in clientes):
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    # Comprobar que el barbero exista
    if not any(b["id"] == cita.barbero_id for b in barberos):
        raise HTTPException(
            status_code=404,
            detail="Barbero no encontrado"
        )

    # Buscar el servicio
    servicio = next(
        (s for s in servicios if s["id"] == cita.servicio_id),
        None
    )

    if servicio is None:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    # Calcular inicio y fin del nuevo horario
    inicio_nuevo = datetime.combine(cita.fecha, cita.hora)
    fin_nuevo = inicio_nuevo + timedelta(
        minutes=servicio["duracion"]
    )

    # Revisar otras citas del mismo barbero
    for existente in citas:

        # Ignorar la cita que estamos modificando
        if existente["id"] == id:
            continue

        if existente["barbero_id"] == cita.barbero_id:

            inicio_existente = datetime.combine(
                date.fromisoformat(existente["fecha"]),
                time.fromisoformat(existente["hora"])
            )

            servicio_existente = next(
                (
                    s for s in servicios
                    if s["id"] == existente["servicio_id"]
                ),
                None
            )

            if servicio_existente is None:
                raise HTTPException(
                    status_code=409,
                    detail="Una cita existente tiene un servicio no disponible"
                )

            fin_existente = inicio_existente + timedelta(
                minutes=servicio_existente["duracion"]
            )

            # Comprobar empalmes
            if inicio_nuevo < fin_existente and fin_nuevo > inicio_existente:
                raise HTTPException(
                    status_code=409,
                    detail="El barbero ya tiene una cita en ese horario"
                )

    # Actualizar los datos
    cita_actual.update(cita.model_dump(mode="json"))

    return {
        "mensaje": "Cita actualizada correctamente",
        "cita": cita_actual
    }
