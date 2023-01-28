import pandas as pd

def remove_not_found():
    file_path = "./dags/files/string/interactions_uniprot_ids.csv"

    interactions = pd.read_csv(file_path)
    print(interactions.columns)
    interactions = interactions[interactions.interactorA != 'Not Found']
    interactions = interactions[interactions.interactorB != 'Not Found']
    interactions.to_csv(file_path, index=False, index_label=False)


if __name__ == '__main__':
    remove_not_found()
