from database import get_db, close_db
from models import Antigen, Antibody, Interaction, Aa_interaction, Antibody_has_aa_interaction

import requests
from requests.exceptions import Timeout, HTTPError, ConnectionError
from time import time

import pandas as pd

from extract_antigens import extract_json_uniprot, extract_fasta
from load_antigens import create_antigen_database_relation

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
    data = db.query(Antibody.id).filter(Antibody.name.like(search)).first()
    close_db(db)
    if data == None:
        return -1
    return data[0]

def download_antigen(antigen, database):
    if database == "uniprotkb":
        uniprot_api = f"https://rest.uniprot.org/uniprotkb/{antigen}.json"
        response = request_with_retry(uniprot_api, 5)
        #JSON
        if not(response):
            return -1
        antigen = extract_json_uniprot(dict(response.json()))
        if len(antigen) == 0:
            return -1
        antigen['database'] = 'UniProt'
        return antigen
    if database != None and "UniProt_ID" in database:
        uniprot_api = f"https://rest.uniprot.org/uniprotkb/stream?format=json&query=%28%28id%3A{antigen}%29%29"
        response = request_with_retry(uniprot_api, 5)
        #JSON
        if not(response):
            return -1
        antigen = extract_json_uniprot(dict(response.json()))
        if len(antigen) == 0:
            return -1
        antigen['database'] = 'UniProt'
        return antigen
        
    if database != None and "kegg" in database:
        kegg_api = f"https://rest.kegg.jp/get/{antigen}/aaseq"
        response = request_with_retry(kegg_api, 5)
        #FASTA, Ligero y complejo
        if not(response):
            return -1
        antigen = extract_fasta(response)
        if len(antigen) == 0:
            return -1
        antigen['database'] = 'KEGG'
        return antigen
    return -1

def create_antigen(antigen):
    antigen_db = Antigen(name=antigen['name'], sequence=antigen['sequence'])
    db = get_db()
    db.add(antigen_db)
    db.commit()
    close_db(db)

def interaction_exist(antibody_id, antigen_id):
    db = get_db()
    data = db.query(Interaction.antigen_id, Interaction.antibody_id).filter(Interaction.antibody_id == antibody_id).filter(Interaction.antigen_id == antigen_id).first()
    close_db(db)
    if data == None:
        return -1
    return data[0]

def create_interaction(antibody_id, antigen_id, score):
    if interaction_exist(antibody_id, antigen_id) != -1:
        return
    interaction = Interaction(antibody_id = antibody_id, antigen_id = antigen_id, score=score)
    db = get_db()
    db.add(interaction)
    db.commit()
    close_db(db)

def ab_interaction_exist(antibody1_id, antibody2_id):
    if antibody1_id < antibody2_id:
        name = f"{antibody1_id}-{antibody2_id}"
    else:
        name = f"{antibody2_id}-{antibody1_id}"
    db = get_db()
    data = db.query(Aa_interaction.id).filter(Aa_interaction.name == name).first()
    close_db(db)
    if data == None:
        return -1
    return data[0]

def create_ab_interaction(antibody1_id, antibody2_id, score):
    if ab_interaction_exist(antibody1_id, antibody2_id) != -1:
        return
    if antibody1_id < antibody2_id:
        name = f"{antibody1_id}-{antibody2_id}"
    else:
        name = f"{antibody2_id}-{antibody1_id}"
    if antibody1_id == antibody2_id:
        interaction_type = "Self"
    else:
        interaction_type = "Anti-Idiotype"
    db = get_db()
    aa_interaction = Aa_interaction(name=name, score=score, type=interaction_type)
    db.add(aa_interaction)
    db.commit()
    close_db(db)
    aa_interaction_id = ab_interaction_exist(antibody1_id = antibody1_id, antibody2_id = antibody2_id)
    db = get_db()
    antibody_has_aa_interaction = Antibody_has_aa_interaction(antibody_id = antibody1_id, aa_interaction_id = aa_interaction_id)
    db.add(antibody_has_aa_interaction)
    db.commit()
    close_db(db)
    if interaction_type == "Self":
        return
    db = get_db()
    antibody_has_aa_interaction = Antibody_has_aa_interaction(antibody_id = antibody2_id, aa_interaction_id = aa_interaction_id)
    db.add(antibody_has_aa_interaction)
    db.commit()
    close_db(db)

def load_interactions(df):

    for index, interaction in df.iterrows():
        if index % 100 == 0:
            print(index)

        interactora = interaction['interactorA']
        interactorb = interaction['interactorB']
        score = interaction['score']

        #Busca a ambos interactores en la tabla de anticuerpos
        interactora_id = get_antibody_id(interactora)
        interactorb_id = get_antibody_id(interactorb)

        #Si ninguno de los dos es un anticuerpo se omite la interaccion
        if interactora_id == -1 and interactorb_id == -1:
            continue

        #Relacion AB - AB
        if interactora_id != -1 and interactorb_id != -1:
            #Crear relacion ab - ab

            create_ab_interaction(interactora_id, interactorb_id, score)
            continue

        #Revisa si el interactor A es el antigeno
        if interactora_id == -1:
            antibody_id = interactorb_id
            antigen_id = get_antigen_id(interactora)
            if antigen_id == -1:
                antigen = download_antigen(interactora, interaction['interactorADB'])
                if antigen != -1:
                    create_antigen(antigen)
                    create_antigen_database_relation(antigen)
                    antigen_id = get_antigen_id(interactora)
                else:
                    continue
        else:
            antibody_id = interactora_id
            antigen_id = get_antigen_id(interactorb)
            if antigen_id == -1:
                antigen = download_antigen(interactorb, interaction['interactorBDB'])
                if antigen != -1:
                    create_antigen(antigen)
                    create_antigen_database_relation(antigen)
                    antigen_id = get_antigen_id(interactorb)
                else: 
                    continue
        create_interaction(antibody_id, antigen_id, score)

if __name__ == '__main__':
    df = pd.read_csv("./datasets/interactions.csv")

    load_interactions(df)
