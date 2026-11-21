import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
#carga las variables desde .env
load_dotenv()
# define la url de la base desde .env
DATABASE_URL = os.getenv("DATABASE_URL")
#crea el motor de conexion con la base
engine = create_engine(DATABASE_URL)
#crea el gestor de sesion
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para obtener la sesión de BD en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()