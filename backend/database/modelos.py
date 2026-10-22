
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base
from sqlalchemy import Date, Time, ForeignKey

Base = declarative_base()


# Tabla de clientes
class ClienteDB(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)


# Tabla de barberos
class BarberoDB(Base):
    __tablename__ = "barberos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)


# Tabla de servicios
class ServicioDB(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    precio = Column(Numeric(10, 2), nullable=False)
    duracion = Column(Integer, nullable=False)

# Tabla de citas
class CitaDB(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    barbero_id = Column(Integer, ForeignKey("barberos.id"), nullable=False)
    servicio_id = Column(Integer, ForeignKey("servicios.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
