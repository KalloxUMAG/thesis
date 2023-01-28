import requests
import time
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


def get_interactor(id, interactors):
    for interactor in interactors:
        if interactor['id'] == id:
            db = interactor['preferred_id_db'].split(' ')[1]
            return {'db_id': interactor['preferred_id'], 'db': db}
    
    return {'db_id': 'NULL', 'db': 'NULL'}


def check_response(response):
    if response.status_code == 200 and response.text.startswith("data")
        return True
    return False

def download():

    max_requests = 2
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
        
        if index%1000==0:
            save_path = f'./dags/files/intact/downloads/interactions{current_save}.csv'
            df.to_csv(save_path, index_label=False, index=False)
            df = pd.DataFrame(columns=df.columns)
            current_save = current_save + 1
        print(index)

    df.to_csv(f'./dags/files/intact/downloads/interactions{current_save}.csv', index_label=False, index=False)


if __name__ == '__main__':
    download()
