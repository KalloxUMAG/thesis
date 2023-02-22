from database import Base, engine

from database import get_db
from sqlalchemy.orm import Session
from models import Database, Epitope, Epitope_has_database

def create_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def obtener_epitopes():
    data = next(get_db()).query(Database.name, Epitope.name).filter(Epitope_has_database.database_id == Database.id).filter(Epitope_has_database.epitope_id == Epitope.id)
    for result in data:
        print(result)

create_tables()
