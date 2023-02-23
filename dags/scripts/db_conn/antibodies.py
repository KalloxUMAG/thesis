from sqlalchemy.orm import Session
from scripts.db_conn.models import Antibody


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

if __name__ == '__main__':
    get_antibody_id('Hola', 'mundo')