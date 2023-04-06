from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
ip = os.getenv('IP')
port = os.getenv('PORT')

DATABASE_URL = f"postgresql://{username}:{password}@{ip}:{port}/{database}"
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Abrir enlace con la base de datos
def get_db():
    db = SessionLocal()
    return db


# Cerrar enlace con la base de datos
def close_db(db):
    db.close()
