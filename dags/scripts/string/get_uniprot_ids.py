import pandas as pd
import os

def get_uniprot_ids():
    file_path = "./dags/files/uniprot/antibodies.csv"

    if os.path.exists(file_path) == False:
        print("Error, file doesn't exist")
        return

    uniprot_dataset = pd.read_csv(file_path)
    uniprot_dataset = uniprot_dataset.drop(columns=['primaryAccession', 'lastSequenceUpdateDate', 'organismScientificName', 'proteinName', 'cdAntigenNames', 'genes', 'functions', 'interactionText', 'sequence', 'pdb', 'alphafolddb', 'intact', 'biogrid', 'naturalVariants'])
    uniprot_dataset.dropna(inplace=True)
    uniprot_dataset.to_csv("./dags/files/string/id_to_search.csv", index=False, index_label=False)


if __name__ == "__main__":
    get_uniprot_ids()
