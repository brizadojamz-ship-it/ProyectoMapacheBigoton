from database.conexion import SessionLocal
from database.modelos import ClienteDB, BarberoDB, ServicioDB

# Tus datos temporales
clientes = [
    {"id": 1, "nombre": "Diana Lozano", "telefono": "2311501210"},
    {"id": 2, "nombre": "Abraham Zamora", "telefono": "2223548909"}
]

barberos = [
    {"id": 1, "nombre": "Diego Ramírez"},
    {"id": 2, "nombre": "Armando Jiménez"},
    {"id": 3, "nombre": "Joaquín Torres"}
]

servicios = [
    {"id": 1, "nombre": "Corte clásico", "descripcion": "Corte de cabello tradicional", "precio": 120.0, "duracion": 30},
    {"id": 2, "nombre": "Corte escolar", "descripcion": "Corte de cabello casquete desvanecido", "precio": 80.0, "duracion": 20},
    {"id": 3, "nombre": "Corte WolfCut", "descripcion": "Corte de moda tendencia 2026", "precio": 150.0, "duracion": 60},
    {"id": 4, "nombre": "Corte de Librito", "descripcion": "Corte que le queda a gente guapa", "precio": 130.0, "duracion": 40}
]

def migrar_datos():
    db = SessionLocal()
    try:
        # Insertar clientes
        for c in clientes:
            if not db.query(ClienteDB).filter_by(id=c["id"]).first():
                db.add(ClienteDB(id=c["id"], nombre=c["nombre"], telefono=c["telefono"]))
        
        # Insertar barberos
        for b in barberos:
            if not db.query(BarberoDB).filter_by(id=b["id"]).first():
                db.add(BarberoDB(id=b["id"], nombre=b["nombre"]))

        # Insertar servicios
        for s in servicios:
            if not db.query(ServicioDB).filter_by(id=s["id"]).first():
                db.add(ServicioDB(id=s["id"], nombre=s["nombre"], descripcion=s["descripcion"], precio=s["precio"], duracion=s["duracion"]))

        db.commit()
        print("¡Todos los datos fueron migrados a MySQL exitosamente!")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrar_datos()