import requests
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


def get_interactor(id, interactors):
    for interactor in interactors:
        if interactor['id'] == id:
            db = interactor['preferred_id_db'].split(' ')[1]
            return {'db_id': interactor['preferred_id'], 'db': db}
    
    return {'db_id': 'NULL', 'db': 'NULL'}

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

        data = requests.post(url, {"identifiers": id})
        data = data.json()
        
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


if __name__ == '__main__':
    download()
