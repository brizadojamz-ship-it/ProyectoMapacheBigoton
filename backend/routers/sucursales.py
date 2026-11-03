from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

from database.conexion import obtener_db
from database.modelos import SucursalDB

router = APIRouter(prefix="/sucursales", tags=["Sucursales"])

# --- Esquemas Pydantic ---
class SucursalBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None

class SucursalRespuesta(SucursalBase):
    id: int
    class Config:
        from_attributes = True

# --- Rutas CRUD ---
@router.get("/", response_model=List[SucursalRespuesta])
def obtener_sucursales(db: Session = Depends(obtener_db)):
    return db.query(SucursalDB).all()

@router.post("/", response_model=SucursalRespuesta)
def crear_sucursal(sucursal: SucursalBase, db: Session = Depends(obtener_db)):
    nueva_sucursal = SucursalDB(**sucursal.model_dump())
    db.add(nueva_sucursal)
    db.commit()
    db.refresh(nueva_sucursal)
    return nueva_sucursal

@router.delete("/{id}")
def eliminar_sucursal(id: int, db: Session = Depends(obtener_db)):
    sucursal = db.query(SucursalDB).filter(SucursalDB.id == id).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    # Aquí podríamos agregar validaciones si la sucursal tiene citas asignadas
    db.delete(sucursal)
    db.commit()
    return {"mensaje": "Sucursal eliminada correctamente"}