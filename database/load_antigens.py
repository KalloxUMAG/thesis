from database import Base, engine

from database import get_db, close_db
from sqlalchemy.orm import Session
from models import Antigen, Database, Antigen_has_database

import pandas as pd

def get_database_id(name):
    db = get_db()
    data = get_db().query(Database.id).filter(Database.name == name).first()
    close_db(db)
    if data == None:
        return -1
    return data[0]

def get_antigen_id(name):
    db = get_db()
    data = db.query(Antigen.id).filter(Antigen.name == name).first()
    close_db(db)
    if data == None:
        return -1
    return data[0]

def create_antigen_database_relation(antigen):
    relations = []

    name = antigen['name']
    database = antigen['database']
    antigen_id = get_antigen_id(name)
    database_id = get_database_id(database)
    if database_id == -1 or antigen_id == -1:
        return
    relation = Antigen_has_database(antigen_id=antigen_id, database_id=database_id)
    relations.append(relation)
    db = get_db()
    db.add_all(relations)
    db.commit()
    close_db(db)

def load_interactions(df):
    
    for index, row in df.iterrows():
        if index < 619676:
            continue
        if index%1000 == 0:
            print(index)
        '''
        exists = get_antigen_id(row['name'])
        if exists != -1:
            continue
        else:
            break
        '''
        antigen = Antigen(name=row['name'], sequence=row['sequence'])
        db = get_db()
        db.add(antigen)
        db.commit()
        close_db(db)
        create_antigen_database_relation(row)

if __name__ == '__main__':
    df = pd.read_csv("./datasets/antigens.csv")

    load_interactions(df)
