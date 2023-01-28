from database import get_db, close_db
from models import Antigen, Antibody, Interaction, Aa_interaction, Antibody_has_aa_interaction

import requests
from requests.exceptions import Timeout, HTTPError, ConnectionError
from time import time

import pandas as pd

def request_with_retry(request, MAX_RETRIES):
    for i in range(MAX_RETRIES):
        try:
            r = requests.get(request, timeout=100)
            r.raise_for_status()
            return r
        except ConnectionError as ce:
            print("Antigen does not exist")
            return False
        except Timeout as tout:
            print(f'TimeOut Error, retrying ({i}/{MAX_RETRIES})')
        except HTTPError as err:
            print(r.status_code)
            if r.status_code == 429:
                print(r.content)
                time.sleep(int(r.headers["Retry-After"])+5)
            else:
                return False
    return False

def get_antigen_id(name):
    search = f'%{name}%'
    db = get_db()
    data = db.query(Antigen.id).filter(Antigen.name.like(search)).first()
    close_db(db)
    if data == None:
        return -1
    return data[0]

def get_antibody_id(name):
    search = f'%{name}%'
    db = get_db()
    data = db.query(Antibody.name).filter(Antibody.name.like(search)).first()
    close_db(db)
    if data == None:
        return -1
    return data[0]



def download_uniprot

def download_antigen(antigen, database):
    if database != None and "uniprot" in database:
        uniprot_api = f"https://rest.uniprot.org/uniprotkb/stream?fields=accession%2Cid%2Cprotein_name%2Csequence&format=tsv&query=%28%28id%3A{antigen}%29%29"
        response = request_with_retry(uniprot_api, 5)
        if response == -1:
            return response
        
    if database != None and "kegg" in database:
        kegg_api = f"https://rest.kegg.jp/get/{antigen}/aaseq"
        response = request_with_retry(kegg_api, 5)
        if response == -1:
            return response
    return -1

def load_inteactions(df):
    
    contador = 0
    for index, interaction in df.iterrows():

        if index%1000 == 0:
            print(index)
            print(contador)

        interactora = interaction['interactorA']
        interactorb = interaction['interactorB']

        interactora_id = get_antibody_id(interactora)
        interactorb_id = get_antibody_id(interactorb)

        if interactora_id == -1 and interactorb_id == -1:
            contador = contador + 1
            continue

        if interactora_id == -1:
            antibody_id = interactorb_id
            antigen = download_antigen(interactora, interaction['interactorADB'])
        else:
            antibody_id = interactora_id
            antigen = download_antigen(interactorb, interaction['interactorBDB'])




df = pd.read_csv("./datasets/interactions.csv")

load_inteactions(df)
