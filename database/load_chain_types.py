from database import get_db, close_db
from sqlalchemy.orm import Session
from models import Chain_type

import pandas as pd

def load_chain_types():
    df = pd.read_csv("./datasets/chain_types.csv")
    db = get_db()
    for index, row in df.iterrows():
        chain_type = Chain_type(name=row['name'])
        
        db.add(chain_type)
    
    db.commit()
    close_db(db)

load_chain_types()