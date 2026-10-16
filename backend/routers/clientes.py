
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import obtener_db
from backend.database import ClienteDB

router = APIRouter(tags=["Clientes"])


class Cliente(BaseModel):
    nombre: str
    telefono: str


# Consultar clientes
@router.get("/clientes")
def obtener_clientes(db: Session = Depends(obtener_db)):
    return db.query(ClienteDB).all()


# Registrar cliente
@router.post("/clientes", status_code=201)
def registrar_cliente(
    cliente: Cliente,
    db: Session = Depends(obtener_db)
):
    nuevo_cliente = ClienteDB(**cliente.model_dump())

    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    return nuevo_cliente


# Actualizar cliente
@router.put("/clientes/{id}")
def actualizar_cliente(
    id: int,
    cliente: Cliente,
    db: Session = Depends(obtener_db)
):
    cliente_db = db.query(ClienteDB).filter(
        ClienteDB.id == id
    ).first()

    if not cliente_db:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    cliente_db.nombre = cliente.nombre
    cliente_db.telefono = cliente.telefono

    db.commit()
    db.refresh(cliente_db)

    return {
        "mensaje": "Cliente actualizado correctamente",
        "cliente": cliente_db
    }


# Eliminar cliente
@router.delete("/clientes/{id}")
def eliminar_cliente(
    id: int,
    db: Session = Depends(obtener_db)
):
    cliente_db = db.query(ClienteDB).filter(
        ClienteDB.id == id
    ).first()

    if not cliente_db:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    db.delete(cliente_db)
    db.commit()

    return {"mensaje": "Cliente eliminado correctamente"}
