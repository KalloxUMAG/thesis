from scripts.db_conn.models import Antigen, Antigen_has_database
from scripts.db_conn.load_databases import get_database_id
from sqlalchemy import or_

def get_antigen_id(name, db):
    search = f"%{name}%"
    data = db.query(Antigen).filter(Antigen.name.like(search)).all()

    if data == None:
        return -1
    for result in data:
        ids = result.name
        if ids == name:
            return result.id
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
    db.add(relation)
    db.commit()

def exist_antigen_database_relation(antigen, db):
    name = antigen["name"]
    database = antigen["database"]
    antigen_id = get_antigen_id(name)
    database_id = get_database_id(database)
    if database_id == -1 or antigen_id == -1:
        return 0
    data = (
        db.query(Antigen_has_database)
        .filter(
            Antigen_has_database.antigen_id == antigen_id,
            Antigen_has_database.database_id == database_id,
        )
        .first()
    )
    if data == None:
        return False
    return True

def load_antigen(antigen, db):

    antigen_db = Antigen(name=antigen["name"], sequence=antigen["sequence"])
    db.add(antigen_db)
    db.commit()
    create_antigen_database_relation(antigen, db)