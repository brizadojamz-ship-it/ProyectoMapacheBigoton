from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Importaciones corregidas
from database.conexion import obtener_db
from database.modelos import (
    ClienteDB,
    BarberoDB,
    ServicioDB,
    CitaDB
)

router = APIRouter(tags=["Agenda y monitoreo"])


# AGENDA DEL DUEÑO
# =====================================

@router.get("/agenda/{fecha}")
def consultar_agenda(
    fecha: date,
    db: Session = Depends(obtener_db)
):

    agenda = []

    # Consultar las citas de la fecha solicitada
    citas_dia = db.query(CitaDB).filter(
        CitaDB.fecha == fecha
    ).all()

    for cita in citas_dia:

        cliente = db.get(ClienteDB, cita.cliente_id)
        barbero = db.get(BarberoDB, cita.barbero_id)
        servicio = db.get(ServicioDB, cita.servicio_id)

        agenda.append({
            "id": cita.id,
            "hora": cita.hora.isoformat(),
            "cliente": cliente.nombre if cliente else "No disponible",
            "barbero": barbero.nombre if barbero else "No disponible",
            "servicio": servicio.nombre if servicio else "No disponible",
            "precio": float(servicio.precio) if servicio else 0
        })

    # Ordenar por hora
    agenda.sort(key=lambda c: c["hora"])

    return agenda


# PANEL DE MONITOREO
# =====================================

@router.get("/resumen/{fecha}")
def obtener_resumen(
    fecha: date,
    db: Session = Depends(obtener_db)
):

    # Consultar citas del día
    citas_dia = db.query(CitaDB).filter(
        CitaDB.fecha == fecha
    ).all()

    # Calcular ingresos estimados
    ingresos = 0

    for cita in citas_dia:

        servicio = db.get(ServicioDB, cita.servicio_id)

        if servicio:
            ingresos += servicio.precio

    # Consultar todos los barberos
    barberos = db.query(BarberoDB).all()

    # Contar citas por barbero
    citas_por_barbero = []

    for barbero in barberos:

        cantidad = sum(
            1 for cita in citas_dia
            if cita.barbero_id == barbero.id
        )

        citas_por_barbero.append({
            "barbero": barbero.nombre,
            "total_citas": cantidad
        })

    return {
        "fecha": fecha.isoformat(),
        "total_citas": len(citas_dia),
        "ingresos_estimados": float(ingresos),
        "citas_por_barbero": citas_por_barbero
    }