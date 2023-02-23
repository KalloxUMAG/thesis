from scripts.db_conn.models import Antigen

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