
from datetime import date, time, datetime, timedelta

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="El Mapache Bigotón")


# =====================================
# MÓDULO DE CLIENTES
# =====================================

clientes = [
    {"id": 1, "nombre": "Diana Lozano", "telefono": "2311501210"},
    {"id": 2, "nombre": "Abraham Zamora", "telefono": "2223548909"}
]


class Cliente(BaseModel):
    nombre: str
    telefono: str


# Consultar clientes
@app.get("/clientes")
def obtener_clientes():
    return clientes


# Registrar cliente
@app.post("/clientes", status_code=201)
def registrar_cliente(cliente: Cliente):
    nuevo_cliente = {
        "id": max((c["id"] for c in clientes), default=0) + 1,
        **cliente.model_dump()
    }

    clientes.append(nuevo_cliente)
    return nuevo_cliente


# Actualizar cliente
@app.put("/clientes/{id}")
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
@app.delete("/clientes/{id}")
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
# MÓDULO DE BARBEROS
# =====================================

barberos = [
    {"id": 1, "nombre": "Diego Ramírez"},
    {"id": 2, "nombre": "Armando Jiménez"},
    {"id": 3, "nombre": "Joaquín Torres"}
]


class Barbero(BaseModel):
    nombre: str


# Consultar barberos
@app.get("/barberos")
def obtener_barberos():
    return barberos


# Registrar barbero
@app.post("/barberos", status_code=201)
def registrar_barbero(barbero: Barbero):
    nuevo_barbero = {
        "id": max((b["id"] for b in barberos), default=0) + 1,
        **barbero.model_dump()
    }

    barberos.append(nuevo_barbero)
    return nuevo_barbero


# Actualizar barbero
@app.put("/barberos/{id}")
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
@app.delete("/barberos/{id}")
def eliminar_barbero(id: int):
    for b in barberos:
        if b["id"] == id:
            barberos.remove(b)

            return {"mensaje": "Barbero eliminado correctamente"}

    raise HTTPException(
        status_code=404,
        detail="Barbero no encontrado"
    )


# =====================================
# MÓDULO DE SERVICIOS
# =====================================

servicios = [
    {
        "id": 1,
        "nombre": "Corte clásico",
        "descripcion": "Corte de cabello tradicional",
        "precio": 120.0,
        "duracion": 30
    },
    {
        "id": 2,
        "nombre": "Corte escolar",
        "descripcion": "Corte de cabello casquete desvanecido",
        "precio": 80.0,
        "duracion": 20
    },
    {
        "id": 3,
        "nombre": "Corte WolfCut",
        "descripcion": "Corte de moda tendencia 2026",
        "precio": 150.0,
        "duracion": 60
    },
    {
        "id": 4,
        "nombre": "Corte de Librito",
        "descripcion": "Corte que le queda a gente guapa",
        "precio": 130.0,
        "duracion": 40
    }
]


class Servicio(BaseModel):
    nombre: str = Field(min_length=1)
    descripcion: str
    precio: float = Field(gt=0)
    duracion: int = Field(gt=0)


# Consultar servicios
@app.get("/servicios")
def obtener_servicios():
    return servicios


# Registrar servicio
@app.post("/servicios", status_code=201)
def registrar_servicio(servicio: Servicio):
    nuevo_servicio = {
        "id": max((s["id"] for s in servicios), default=0) + 1,
        **servicio.model_dump()
    }

    servicios.append(nuevo_servicio)
    return nuevo_servicio


# Actualizar servicio
@app.put("/servicios/{id}")
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
@app.delete("/servicios/{id}")
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
# MÓDULO DE CITAS
# =====================================

citas = []


class Cita(BaseModel):
    cliente_id: int
    barbero_id: int
    servicio_id: int
    fecha: date
    hora: time


# Consultar todas las citas
@app.get("/citas")
def obtener_citas():
    return citas


# Registrar una cita
@app.post("/citas", status_code=201)
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


# =====================================
# INICIO
# =====================================

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a El Mapache Bigotón"}

#Eliminar
@app.delete("/citas/{id}")
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


@app.put("/citas/{id}")
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

# AGENDA DEL DUEÑO
# =====================================

@app.get("/agenda/{fecha}")
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

@app.get("/resumen/{fecha}")
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
