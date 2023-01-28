from database import Base, engine

from database import get_db, close_db
from sqlalchemy.orm import Session
from models import Database

import pandas as pd

def load_databases():
    df = pd.read_csv("./datasets/databases.csv")
    db = get_db()
    for index, row in df.iterrows():
        database = Database(name=row['name'])
        
        db.add(database)
    
    db.commit()
    close_db(db)

load_databases()