import pandas as pd
from scripts.db_conn.database import get_db, close_db
from scripts.db_conn.antibodies import get_antibody_id
from scripts.db_conn.antigens import get_antigen_id
from scripts.db_conn.epitopes import get_epitope_id

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

def remove_existing_epitopes(df):
    db = get_db()
    for index, epitope in df.iterrows():
        exist = get_epitope_id(epitope['name'], db)
        if exist != -1:
            df = df.drop(index)
    close_db(db)
    return df

def remove_existing_interaction(df):
    return