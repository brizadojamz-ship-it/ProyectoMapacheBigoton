from datetime import date
from fastapi import APIRouter
from backend.datos import citas, clientes, barberos, servicios

router = APIRouter(tags=["Agenda y monitoreo"])

# AGENDA DEL DUEÑO
# =====================================

@router.get("/agenda/{fecha}")
def consultar_agenda(fecha: date):

    agenda = []

    for cita in citas:

        if cita["fecha"] == fecha.isoformat():

            cliente = next(
                (c for c in clientes if c["id"] == cita["cliente_id"]),
                None
            )

            barbero = next(
                (b for b in barberos if b["id"] == cita["barbero_id"]),
                None
            )

            servicio = next(
                (s for s in servicios if s["id"] == cita["servicio_id"]),
                None
            )

            agenda.append({
                "id": cita["id"],
                "hora": cita["hora"],
                "cliente": cliente["nombre"] if cliente else "No disponible",
                "barbero": barbero["nombre"] if barbero else "No disponible",
                "servicio": servicio["nombre"] if servicio else "No disponible",
                "precio": servicio["precio"] if servicio else 0
            })

    agenda.sort(key=lambda c: c["hora"])

    return agenda

# PANEL DE MONITOREO
# =====================================

@router.get("/resumen/{fecha}")
def obtener_resumen(fecha: date):

    # Buscar las citas del día
    citas_dia = [
        c for c in citas
        if c["fecha"] == fecha.isoformat()
    ]

    # Calcular los ingresos estimados
    ingresos = 0

    for cita in citas_dia:
        servicio = next(
            (s for s in servicios if s["id"] == cita["servicio_id"]),
            None
        )

        if servicio:
            ingresos += servicio["precio"]

    # Contar citas por barbero
    citas_por_barbero = []

    for barbero in barberos:
        cantidad = sum(
            1 for c in citas_dia
            if c["barbero_id"] == barbero["id"]
        )

        citas_por_barbero.append({
            "barbero": barbero["nombre"],
            "total_citas": cantidad
        })

    return {
        "fecha": fecha.isoformat(),
        "total_citas": len(citas_dia),
        "ingresos_estimados": ingresos,
        "citas_por_barbero": citas_por_barbero
    }
