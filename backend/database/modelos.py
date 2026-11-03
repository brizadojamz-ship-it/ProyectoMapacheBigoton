from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey
from database.conexion import Base

class SucursalDB(Base):
    __tablename__ = "sucursales"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(255))
    telefono = Column(String(20))


class ClienteDB(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20))
    # Relación con la sucursal
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable=True)


class BarberoDB(Base):
    __tablename__ = "barberos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    # Relación con la sucursal
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable=True)


class ServicioDB(Base):
    __tablename__ = "servicios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    precio = Column(Float, nullable=False)
    duracion = Column(Integer, nullable=False)


class CitaDB(Base):
    __tablename__ = "citas"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    barbero_id = Column(Integer, ForeignKey("barberos.id"), nullable=False)
    servicio_id = Column(Integer, ForeignKey("servicios.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    # Relación con la sucursal
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable=True)