from sqlalchemy.orm import Session
from scripts.db_conn.models import Antibody, Antibody_has_database, Antibody_chain, Chain_type
from scripts.db_conn.load_databases import get_database_id


# Obtener Id del Antibody o -1 si no existe
def get_antibody_id(name, db):
    search = f"%{name}%"
    #db = get_db()
    data = db.query(Antibody).filter(Antibody.name.like(search)).all()
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

#Crear relacion entre el anticuerpo y el antigeno
def create_antibody_database_relation(antibody, db):
    name = antibody["name"]
    database = antibody["database"]
    antibody_id = get_antibody_id(name, db)
    database_id = get_database_id(database, db)
    if database_id == -1 or antibody_id == -1:
        return
    relation = Antibody_has_database(antibody_id=antibody_id, database_id=database_id)
    db.add(relation)
    db.commit()

def create_antibody_chain(antibody, antibody_id, db):
    chains = ['light_sequence', 'heavy_sequence', 'cdrh3', 'cdrl3', 'cdr3', 'sequence']

    if not 'ss3' in antibody.columns:
        antibody['ss3'] = ''
    if not 'ss8' in antibody.columns:
        antibody['ss8'] = ''

    for chain in chains:
        if chain in antibody.columns:
            antibody_chain_db = Antibody_chain(name=antibody['name'], sequence=antibody[chain], length=len(antibody[chain]), ss3=antibody['ss3'], ss8=antibody['ss8'], antibody_id=antibody_id)
            db.add(antibody_chain_db)
            db.commit()

#Cargar anticuerpo en la base de datos y luego crear la relacion con la base de datos
def load_antibody(antibody, db):

    antibody_db = Antibody(name=antibody["name"])
    db.add(antibody_db)
    db.commit()
    create_antibody_database_relation(antibody, db)
    create_antibody_chain(antibody, antibody_db.id, db)

if __name__ == '__main__':
    get_antibody_id('Hola', 'mundo')