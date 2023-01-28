import pandas as pd
import numpy as np


def is_in(below_limit, upper_limit, value):
    below_limit = int(below_limit)
    upper_limit = int(upper_limit)
    value = int(value.split(".")[0])

    print(below_limit, upper_limit, value)

    if below_limit <= value and upper_limit >= value:
        return True
    return False


def found_database_id(value, dataset):
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
    '''
    to_remove = []
    for id in string_ids:
        id_references = uniprot_dataset.loc[uniprot_dataset["string"] == id]
        
        if not(id_references.empty):
            print(id_references["uniProtkbId"])
            print(id)
            dataset["interactorA"] = dataset["interactorA"].replace([id], id_references["uniProtkbId"])
            #dataset["interactorB"] = dataset["interactorB"].replace([id], id_references["uniProtkbId"])
            to_remove.append(id)

    dataset.to_csv("./dags/files/string/interactions_uniprot_ids.csv", index=False, index_label=False)
    '''
    block = 0
        #id_references = uniprot_dataset.loc[uniprot_dataset['string'] == id]
        #if id_references.empty:
        #    print("Not found in antibodies.csv")
    id_index = 0
    for data in string_dataset:
        below_value = data['#string_protein_id'].iloc[0]
        below_value = below_value.split(".")[0]
        upper_value = data['#string_protein_id'].iloc[-1]
        upper_value = upper_value.split(".")[0]

        #if id_index == len(string_ids):
        if id_index == 100:
            break

        for id in string_ids[id_index: -1]:
            if id_index == 100:
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

    dataset.to_csv("./dags/files/string/interactions_uniprot_ids.csv", index=False, index_label=False)



if __name__ == "__main__":
    string_to_db()
