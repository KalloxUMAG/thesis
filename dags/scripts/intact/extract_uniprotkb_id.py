import pandas as pd
import numpy as np
import json

def get_ids(interactions):
    new_interactors = np.array([])
    for index, interaction in interactions.iterrows():
        interactors = interaction['interactors'][1:-1]
        interactors = interactors.split('},')
        for interactor in interactors:
            if len(interactor) > 0 and interactor[-1] != '}':
                interactor = interactor + '}'
            if len(interactor) > 0:
                interactor = interactor.replace("\'", "\"")
                interactor = json.loads(interactor)
                interactor = interactor['preferred_id_db'].split(' ')
                if interactor[1] == '(uniprotkb)':
                    new_interactors = np.append(new_interactors, interactor[0])
            else:
                print(index)
                print(interaction['uniprot id'])
    print(len(new_interactors))
    new_interactors = np.unique(new_interactors)
    print(len(new_interactors))
    df = pd.DataFrame(new_interactors, columns=["uniprot id"])
    df.to_csv('./new_csv.csv', index_label=False, index=False)


def get_interactions(interactions_file):
    new_interactions = np.array([])
    for index, row in interactions_file.iterrows():
        interactions = row['interactions'][1:-1]
        interactions = interactions.split('},')
        for interaction in interactions:
            if len(interaction) > 0 and interaction[-1] != '}':
                interaction = interaction + '}'
            if len(interaction) > 0:
                interaction = interaction.replace("\'", "\"")
                interaction = interaction.replace("False", "false")
                interaction = interaction.replace("True", "true")
                interaction = json.loads(interaction)
                print(interaction)
            else:
                print(index)


def extract():
    interactions_file = './dags/files/intact/downloads/interactions.csv'
    interactions_file = '../../files/intact/downloads/interactions.csv'
    interactions = pd.read_csv(interactions_file).drop(columns=['id', 'intact id'])
    #get_ids(interactions)
    get_interactions(interactions)


if __name__ == '__main__':
    extract()
