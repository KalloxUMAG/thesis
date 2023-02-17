import pandas as pd
import os
import re
import time
import warnings
import requests

warnings.simplefilter(action='ignore', category=FutureWarning)

def get_uniprot_ids():
    file_path = "./dags/files/uniprot/antibodies.csv"

    if os.path.exists(file_path) == False:
        print("Error, file doesn't exist")
        return

    uniprot_dataset = pd.read_csv(file_path)
    uniprot_dataset = uniprot_dataset.drop(columns=['primaryAccession', 'lastSequenceUpdateDate', 'organismScientificName', 'proteinName', 'cdAntigenNames', 'genes', 'functions', 'interactionText', 'sequence', 'pdb', 'alphafolddb', 'string', 'biogrid', 'naturalVariants'])
    uniprot_dataset.dropna(inplace=True)
    uniprot_dataset.to_csv("./dags/files/intact/id_to_search.csv", index=False, index_label=False)

def get_interactor(id, interactors):
    for interactor in interactors:
        if interactor['id'] == id:
            db = interactor['preferred_id_db'].split(' ')[1]
            return {'db_id': interactor['preferred_id'], 'db': db}
    
    return {'db_id': 'NULL', 'db': 'NULL'}

def download():
    max_requests = 100
    request_interval = 60

    current_save = 0

    df = pd.DataFrame(columns=['source', 'target', 'source_db', 'target_db', 'interaction_id', 'interaction_ac',
                    'interaction_type', 'interaction_detection_method', 'interaction_affected_mutation', 'interaction_score', 'interaction_negative'])
    dataset = pd.read_csv('./dags/files/intact/id_to_search.csv')

    url = 'https://www.ebi.ac.uk/intact/ws/network/getInteractions?maxMIScore=1&minMIScore=0&negativeFilter=POSITIVE_ONLY&page=0&pageSize=2147483647&query='

    for index, row in dataset.iterrows():
        if(index!=0 and index%max_requests == 0):
            time.sleep(request_interval)
            print(f'{index} inicia descanso')
        uniprot = row['uniProtkbId']
        id = row['intact']
        data = requests.post(url+id)
        interactions = []
        interactors = []

        data = data.json()
        data = data['data']
        for item in data:
            if item['group'] == 'nodes':
                interactors.append({'id': item['data']['id'],
                                    'preferred_id': item['data']['preferred_id'],
                                    'preferred_id_db': item['data']['preferred_id_db']
                                    })
            if item['group'] == 'edges':
                interactions.append({'id': item['data']['id'],
                                     'source': item['data']['source'],
                                     'target': item['data']['target'],
                                     'interaction_ac': item['data']['interaction_ac'],
                                     'interaction_type': item['data']['interaction_type'],
                                     'interaction_detection_method': item['data']['interaction_detection_method'],
                                     'affected_by_mutation': item['data']['affected_by_mutation'],
                                     'mi_score': item['data']['mi_score'],
                                     'negative': item['data']['negative']
                                     })

        for interaction in interactions:
            interactor_1 = get_interactor(interaction['source'], interactors)
            interactor_2 = get_interactor(interaction['target'], interactors)

            df = df.append({'source': interactor_1['db_id'], 'target': interactor_2['db_id'], 'source_db': interactor_1['db'], 'target_db': interactor_2['db'],
                            'interaction_id': interaction['id'], 'interaction_ac': interaction['interaction_ac'],'interaction_type': interaction['interaction_type'],
                            'interaction_detection_method': interaction['interaction_detection_method'], 'interaction_affected_mutation': interaction['affected_by_mutation'], 
                            'interaction_score': interaction['mi_score'], 'interaction_negative': interaction['negative'],}, ignore_index=True)
        
        if index%999==0 and index!=0:
            save_path = f'./dags/files/intact/downloads/interactions{current_save}.csv'
            df.to_csv(save_path, index_label=False, index=False)
            df = pd.DataFrame(columns=df.columns)
            current_save = current_save + 1
        print(index)

    df.to_csv(f'./dags/files/intact/downloads/interactions{current_save}.csv', index_label=False, index=False)

def remove_duplicates_interactions(df):
    for index, row in df.iterrows():
        df = df[(df.InteractorA != row['InteractorB']) | (df.InteractorB != row['InteractorA'])]
    return df

def join_interactions():

    folder = "./dags/files/intact/downloads/"
    interactions = pd.DataFrame()

    interactions_files = [f for f in os.listdir(folder) if re.match(r'[a-zA-Z0-9]*\.csv', f)]

    for interactions_file in interactions_files:
        print(folder+interactions_file)
        df = pd.read_csv(folder+interactions_file)
        df = df.drop(columns=['interaction_id', 'interaction_ac', 'interaction_type', 'interaction_detection_method', 'interaction_affected_mutation', 'interaction_negative'])
        df.columns = ['InteractorA', 'InteractorB', 'InteractorADB', 'InteractorBDB', 'score']
        df['InteractorADB'] = df['InteractorADB'].str.replace('(', '')
        df['InteractorADB'] = df['InteractorADB'].str.replace(')', '')
        df['InteractorBDB'] = df['InteractorBDB'].str.replace('(', '')
        df['InteractorBDB'] = df['InteractorBDB'].str.replace(')', '')
        print("Drop duplicates")
        df = remove_duplicates_interactions(df)
        print("Join file and drop duplicates")
        interactions = pd.concat([interactions, df]).drop_duplicates(subset=['InteractorA', 'InteractorB'], keep='last').reset_index(drop=True)
        os.remove(folder+interactions_file)

    interactions.to_csv("./dags/files/intact/interactions.csv", index=False, index_label=False)                       

if __name__ == '__main__':
    get_uniprot_ids()