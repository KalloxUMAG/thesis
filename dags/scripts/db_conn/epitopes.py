from scripts.db_conn.models import Epitope, Epitope_has_database
from scripts.db_conn.load_databases import get_database_id

def get_epitope_id(name, db):
    #db = get_db()
    data = db.query(Epitope).filter(Epitope.name == name).first()
    #close_db(db)
    if data == None:
        return -1
    return data[0]

def create_epitope_database_relation(epitope, db):
    name = epitope["name"]
    database = epitope["database"]
    epitope_id = get_epitope_id(name, db)
    database_id = get_database_id(database, db)
    if database_id == -1 or epitope_id == -1:
        return
    relation = Epitope_has_database(epitope_id=epitope_id, database_id=database_id)
    db.add(relation)
    db.commit()

def load_epitope(epitope, db):
    epitope_db = Epitope(name=epitope['name'], sequence=epitope['sequence'])
    db.add(epitope_db)
    db.commit()
    create_epitope_database_relation(epitope, db)