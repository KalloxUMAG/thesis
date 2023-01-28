from database import Base, engine

from database import get_db, close_db
from sqlalchemy.orm import Session
from models import Antibody, Antibody_chain, Database, Antibody_has_database, Chain_type

import pandas as pd

def get_database_id(name):
    db = get_db()
    data = get_db().query(Database.id).filter(Database.name == name).first()
    close_db(db)
    if data == None:
        return -1
    return data[0]

def get_antibody_id(name):
    db = get_db()
    data = db.query(Antibody.id).filter(Antibody.name == name).first()
    close_db(db)
    if data == None:
        return -1
    return data[0]

def get_chain_type_id(name):
    db = get_db()
    data = get_db().query(Chain_type.id).filter(Chain_type.name == name).first()
    close_db(db)
    if data == None:
        return -1
    return data[0]

def exists_antibody_database(antibody_id, database_id):
    db = get_db()
    data = db.query(Antibody_has_database.antibody_id).filter(Antibody_has_database.antibody_id == antibody_id).filter(Antibody_has_database.database_id == database_id).first()
    close_db(db)
    if data == None:
        return False
    return True

def create_antibody_database_relation(antibody):
    relations = []

    name = antibody['name']
    database = antibody['database']
    antibody_id = get_antibody_id(name)
    database_id = get_database_id(database)
    if database_id == -1 or antibody_id == -1:
        return
    relation = Antibody_has_database(antibody_id=antibody_id, database_id=database_id)
    relations.append(relation)
    db = get_db()
    db.add_all(relations)
    db.commit()
    close_db(db)

def create_antibody_chain(antibody):

    antibody_chains = []

    antibody_name = antibody['name']
    antibody_id = get_antibody_id(antibody['name'])


    if antibody['sequence'] != '-':
        sequence = antibody['sequence']
        chain_type_id = get_chain_type_id('Canonical')
        antibody_chain = Antibody_chain(name=f'{antibody_name} | Canonical', sequence=sequence, length=len(sequence), antibody_id=antibody_id, chain_type_id=chain_type_id)
        antibody_chains.append(antibody_chain)
    
    if antibody['light_sequence'] != '-':
        sequence = antibody['light_sequence']
        chain_type_id = get_chain_type_id('Light')
        antibody_chain = Antibody_chain(name=f'{antibody_name} | Light', sequence=sequence, length=len(sequence), antibody_id=antibody_id, chain_type_id=chain_type_id)
        antibody_chains.append(antibody_chain)


    if antibody['heavy_sequence'] != '-':
        sequence = antibody['heavy_sequence']
        chain_type_id = get_chain_type_id('Heavy')
        antibody_chain = Antibody_chain(name=f'{antibody_name} | Heavy', sequence=sequence, length=len(sequence), antibody_id=antibody_id, chain_type_id=chain_type_id)
        antibody_chains.append(antibody_chain)

    if antibody['cdrh3'] != '-':
        sequence = antibody['cdrh3']
        chain_type_id = get_chain_type_id('CDR3 Heavy')
        antibody_chain = Antibody_chain(name=f'{antibody_name} | CDR3 Heavy', sequence=sequence, length=len(sequence), antibody_id=antibody_id, chain_type_id=chain_type_id)
        antibody_chains.append(antibody_chain)

    if antibody['cdrl3'] != '-':
        sequence = antibody['cdrl3']
        chain_type_id = get_chain_type_id('CDR3 Light')
        antibody_chain = Antibody_chain(name=f'{antibody_name} | CDR3 Light', sequence=sequence, length=len(sequence), antibody_id=antibody_id, chain_type_id=chain_type_id)
        antibody_chains.append(antibody_chain)

    if antibody['cdr3'] != '-':
        sequence = antibody['cdr3']
        chain_type_id = get_chain_type_id('CDR3')
        antibody_chain = Antibody_chain(name=f'{antibody_name} | CDR3', sequence=sequence, length=len(sequence), antibody_id=antibody_id, chain_type_id=chain_type_id)
        antibody_chains.append(antibody_chain)

    db = get_db()
    db.add_all(antibody_chains)
    db.commit()
    close_db(db)

def load_antibodies(df):
    
    for index, row in df.iterrows():

        if index%1000 == 0:
            print(index)

        antibody = Antibody(name=row['name'])

        db = get_db()
        db.add(antibody)
        db.commit()
        close_db(db)
        create_antibody_chain(row)
        create_antibody_database_relation(row)


df = pd.read_csv("./datasets/antibodies.csv")

load_antibodies(df)
