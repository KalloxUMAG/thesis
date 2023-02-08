from database import Base, engine

from database import get_db, close_db
from sqlalchemy.orm import Session
from models import Antigen, Database, Antigen_has_database

import pandas as pd

from load_databases import get_database_id


def get_antigen_id(name, db):
    search = f"%{name}%"
    #db = get_db()
    data = db.query(Antigen).filter(Antigen.name.like(search)).all()
    #close_db(db)

    if data == None:
        return -1
    for result in data:
        ids = result.name
        ids = ids.replace(" ", "")
        ids = ids.split("||")
        for id in ids:
            if name == id:
                return result.id
    return -1


def create_antigen_database_relation(antigen, db):
    name = antigen["name"]
    database = antigen["database"]
    antigen_id = get_antigen_id(name, db)
    database_id = get_database_id(database, db)
    if database_id == -1 or antigen_id == -1:
        return
    relation = Antigen_has_database(antigen_id=antigen_id, database_id=database_id)
    #db = get_db()
    db.add(relation)
    db.commit()
    #close_db(db)


def exist_antigen_database_relation(antigen, db):
    name = antigen["name"]
    database = antigen["database"]
    antigen_id = get_antigen_id(name)
    database_id = get_database_id(database)
    if database_id == -1 or antigen_id == -1:
        return 0
    #db = get_db()
    data = (
        db.query(Antigen_has_database)
        .filter(
            Antigen_has_database.antigen_id == antigen_id,
            Antigen_has_database.database_id == database_id,
        )
        .first()
    )
    #close_db(db)
    if data == None:
        return False
    return True


def load_antigen(antigen, db):
    
    exists = get_antigen_id(antigen)
    if exists != -1:
        return

    antigen_db = Antigen(name=antigen["name"], sequence=antigen["sequence"])
    #db = get_db()
    db.add(antigen_db)
    db.commit()
    #close_db(db)
    create_antigen_database_relation(antigen, db)


if __name__ == "__main__":
    df = pd.read_csv("./datasets/antigens.csv")

    for index, row in df.iterrows():
        if index % 1000 == 0:
            print(index)

        load_antigen(row)
