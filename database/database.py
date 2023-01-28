from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


username = "kallox"
password = "Claudioxx124"
database = "alchemy"
ip = "localhost"
port = 5432

DATABASE_URL = f'postgresql://{username}:{password}@{ip}:{port}/{database}'
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    #Obtener sesion a la base de datos y cerrarla
    db = SessionLocal()
    return db

def close_db(db):
    db.close()
