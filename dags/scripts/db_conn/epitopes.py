from scripts.db_conn.models import Epitope

def get_epitope_id(name, db):
    #db = get_db()
    data = db.query(Epitope).filter(Epitope.name == name).first()
    #close_db(db)
    if data == None:
        return -1
    return data[0]