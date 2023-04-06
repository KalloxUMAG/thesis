import pandas as pd
from scripts.db_conn.database import get_db, close_db
from scripts.db_conn.antigens import load_antigen
from scripts.db_conn.antibodies import load_antibody
from scripts.db_conn.epitopes import load_epitope
from scripts.db_conn.gos import create_go
from scripts.db_conn.load_interactions import load_interaction

def load_antigens_db(df):
    db = get_db()
    for index, antigen in df.iterrows():
        load_antigen(antigen, db)
        print(index)
    close_db(db)

def load_antibodies_db(df):
    db = get_db()
    for index, antibody in df.iterrows():
        load_antibody(antibody, db)
        print(index)
    close_db(db)

def load_epitopes_db(df):
    db = get_db()
    for index, epitope in df.iterrows():
        load_epitope(epitope, db)
        print(index)
    close_db(db)

#Cambiar
def load_interactions_db(df):
    db = get_db()
    for index, interaction in df.iterrows():
        load_interaction(interaction, db)
        print(index)
    close_db(db)

def load_go_db(df):
    db = get_db()
    for index, go in df.iterrows():
        create_go(go, db)
        print(index)
    close_db(db)