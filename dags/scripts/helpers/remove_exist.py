import pandas as pd
from db_conn.database import get_db, close_db
from db_conn.antibodies import get_antibody_id
from db_conn.antigens import get_antigen_id

def remove_existing_antibodies(df):
    db = get_db()
    for index, antibody in df.iterrows():
        exist = get_antibody_id(antibody['name'], db)
        if exist != -1:
            df = df.drop(index)
    close_db(db)
    return df

def remove_existing_antigens(df):
    db = get_db()
    for index, antigen in df.iterrows():
        exist = get_antigen_id(antigen['name'], db)
        if exist != -1:
            df = df.drop(index)
    close_db(db)
    return df

def remove_existing_epitope(df):
    return

def remove_existing_interaction(df):
    return