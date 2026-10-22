import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

# Cargar las variables del archivo .env (si existe)
ruta_env = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ruta_env)

# Configuración de la conexión a MySQL (con los datos predeterminados que creamos)
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER", "mapache"),
    password=os.getenv("DB_PASSWORD", "mapache123"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME", "mapache_bigoton"),
)

# Crear el motor de conexión
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Crear sesiones para trabajar con la base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Proporcionar una sesión a los endpoints
def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Probar la conexión con MySQL
if __name__ == "__main__":
    try:
        with engine.connect() as conexion:
            resultado = conexion.execute(text("SELECT DATABASE()"))
            print("¡Conexión exitosa a MySQL!")
            print("Base de datos:", resultado.scalar())
    except Exception as error:
        print("Error al conectar con MySQL:")
        print(error)
