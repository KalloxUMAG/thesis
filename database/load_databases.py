from database import Base, engine

from database import get_db, close_db
from sqlalchemy.orm import Session
from models import Database

import pandas as pd

# Obtener Id de base de datos segun su nombre
def get_database_id(name):
    db = get_db()
    data = db.query(Database.id).filter(Database.name == name).first()
    close_db(db)
    if data == None:
        return -1
    return data[0]


# Crear base de datos con su nombre
def load_database(database_name):
    database = Database(name=database_name)
    db = get_db()
    db.add(database)
    db.commit()
    close_db(db)


# Ejecucion para carga de todas las bases de datos base
if __name__ == "__main__":
    df = pd.read_csv("./datasets/databases.csv")
    for index, row in df.iterrows():
        name = row["name"]
        if get_database_id(name) == -1:
            load_database(name)
