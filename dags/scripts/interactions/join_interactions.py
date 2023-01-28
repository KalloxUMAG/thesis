import pandas as pd

def join_interactions():
    intact_interactions_path = "./dags/files/intact/downloads/interactions.csv"
    string_interactions_path = "./dags/files/string/interactions.csv"

    intact_interactions = pd.read_csv(intact_interactions_path)
    string_interactions = pd.read_csv(string_interactions_path)

    intact_interactions.columns = ['interactorA', 'interactorB', 'interactorADB', 'interactorBDB', 'score']
    intact_interactions['interactionDB'] = 'IntAct'

    string_interactions.columns = ['interactorA', 'interactorB', 'score', 'interactorADB',
       'interactorBDB']
    string_interactions['interactionDB'] = 'String'
    

    interactions = pd.concat([intact_interactions, string_interactions], axis=0)

    interactions = interactions.drop_duplicates()

    interactions.to_csv('./dags/files/interactions/joined_interactions.csv', index=False, index_label=False)    


if __name__ == '__main__':
    join_interactions()
