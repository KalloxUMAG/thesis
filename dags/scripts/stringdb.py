import numpy as np
import pandas as pd
import os
import warnings

from scripts.helpers.requests import post_request_with_retry

warnings.simplefilter(action='ignore', category=FutureWarning)


def get_uniprot_ids():
    file_path = "./dags/files/uniprot/antibodies.csv"

    if os.path.exists(file_path) == False:
        print("Error, file doesn't exist")
        return

    uniprot_dataset = pd.read_csv(file_path)
    uniprot_dataset = uniprot_dataset.drop(columns=['primaryAccession', 'lastSequenceUpdateDate', 'organismScientificName', 'proteinName', 'cdAntigenNames', 'genes', 'functions', 'interactionText', 'sequence', 'pdb', 'alphafolddb', 'intact', 'biogrid', 'naturalVariants'])
    uniprot_dataset.dropna(inplace=True)
    uniprot_dataset.to_csv("./dags/files/string/id_to_search.csv", index=False, index_label=False)

def download():
    df = pd.DataFrame(columns=['interactorA', 'interactorB', 'score'])
    dataset = pd.read_csv('./dags/files/string/id_to_search.csv')

    url = 'https://string-db.org/api/json/network'

    for index, row in dataset.iterrows():
        uniprot = row['uniProtkbId']
        id = row['string']
        interactor_1 = ""
        interactor_2 = ""
        score = 0

        #data = requests.post(url, {"identifiers": id})
        response = post_request_with_retry(url, 5, id)
        if not (response):
            print(f'Could not download the interactions {id} from {url}.')
            continue
        data = response.json()
        
        interaction_number = 0
        for interaction in data:
            interaction_number = interaction_number + 1
            if interaction_number % 2 == 0:
                continue
            interactor_1 = interaction['stringId_A']
            interactor_2 = interaction['stringId_B']
            score = interaction['score']

            df = df.append({'interactorA': interactor_1, 'interactorB': interactor_2, 'score': score}, ignore_index=True)
        
        print(index)
    
    df.to_csv('./dags/files/string/downloads/interactions.csv', index=False, index_label=False)

def remove_not_found():
    file_path = "./dags/files/string/interactions.csv"

    interactions = pd.read_csv(file_path)
    interactions = interactions[interactions.interactorA != 'Not Found']
    interactions = interactions[interactions.interactorB != 'Not Found']
    interactions.to_csv(file_path, index=False, index_label=False)

def is_in(below_limit, upper_limit, value):
    #Ve si el id del organismo esta entre el id mas bajo y el mas alto del chunk tomado (no lo busca)
    below_limit = int(below_limit)
    upper_limit = int(upper_limit)
    value = int(value.split(".")[0])

    if below_limit <= value and upper_limit >= value:
        return True
    return False


def found_database_id(value, dataset):
    #La base de datos del interactor debe corresponder a una de las siguientes
    database_field = ['BLAST_UniProt_ID', 'BLAST_KEGG_KEGGID', 'Ensembl_protein_id', 'Ensembl_HGNC_HGNC_ID']
    id_references = dataset.loc[dataset['#string_protein_id'] == value]

    for field in database_field:
        database_id = id_references.loc[id_references['source'] == field]
        if not(database_id.empty):
            return [database_id["alias"].iloc[0], field]
    return ["Not Found", "Not Found"]


def string_to_db():
    file_path = "./dags/files/string/downloads/interactions.csv"
    uniprot_ids = "./dags/files/string/id_to_search.csv"
    string_data_path = "./dags/files/string/downloads/protein_aliases.txt"

    dataset = pd.read_csv(file_path)
    uniprot_dataset = pd.read_csv(uniprot_ids)
    string_dataset = pd.read_csv(string_data_path, sep='\t', chunksize=10000000)

    dataset["interactorADB"] = dataset["interactorA"]
    dataset["interactorBDB"] = dataset["interactorB"]

    string_ids1 = dataset[["interactorA"]].to_numpy()
    string_ids2 = dataset[["interactorB"]].to_numpy()
    string_ids = np.concatenate((string_ids1, string_ids2), axis=0)
    string_ids = np.unique(string_ids)
    string_ids_organism = lambda t: t.split(".")[0]
    string_ids_helper = np.array([int(string_ids_organism(xi)) for xi in string_ids])
    string_ids = string_ids[np.argsort(string_ids_helper)]
    print(len(string_ids))

    #Leer y reemplazar valores del id_to_search en el dataset
    for index, data in uniprot_dataset.iterrows():
        if index % 1000 == 0:
            print(index)
        string_id = data['string']
        uniprot_id = data['uniProtkbId']
        np_index = np.where(string_ids == string_id)[0]

        if len(np_index) > 0:
            string_ids = np.delete(string_ids, np_index[0])
            dataset["interactorA"] = dataset["interactorA"].replace([string_id], uniprot_id)
            dataset["interactorB"] = dataset["interactorB"].replace([string_id], uniprot_id)
            dataset["interactorADB"] = dataset["interactorADB"].replace([string_id], 'UniProt')
            dataset["interactorBDB"] = dataset["interactorBDB"].replace([string_id], 'UniProt')
    
    print(len(string_ids))
    
    #indice del numpy array
    id_index = 0
    for data in string_dataset:
        #Id de los organismos en el chunk
        below_value = data['#string_protein_id'].iloc[0]
        below_value = below_value.split(".")[0]
        upper_value = data['#string_protein_id'].iloc[-1]
        upper_value = upper_value.split(".")[0]

        if id_index == len(string_ids):
            break

        for id in string_ids[id_index: -1]:
            if id_index == len(string_ids):
                break
            is_in_result = is_in(below_value, upper_value, id)
            print(is_in_result)
            if is_in_result:
                database_id = found_database_id(id, data)
                id_index = id_index + 1
                print(id_index)
                print(database_id)
                dataset["interactorA"] = dataset["interactorA"].replace([id], database_id[0])
                dataset["interactorB"] = dataset["interactorB"].replace([id], database_id[0])
                dataset["interactorADB"] = dataset["interactorADB"].replace([id], database_id[1])
                dataset["interactorBDB"] = dataset["interactorBDB"].replace([id], database_id[1])
            else:
                break

    dataset['interactorADB'] = dataset['interactorADB'].replace(["uniprotkb", "BLAST_UniProt_ID", "BLAST_KEGG_KEGGID"],["UniProt", "UniProt", "KEGG"])
    dataset['interactorBDB'] = dataset['interactorBDB'].replace(["uniprotkb", "BLAST_UniProt_ID", "BLAST_KEGG_KEGGID"],["UniProt", "UniProt", "KEGG"])
    dataset.to_csv("./dags/files/string/interactions.csv", index=False, index_label=False)

if __name__ == '__main__':
    remove_not_found()