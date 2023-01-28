import pandas as pd

def drop_uniprot_columns():
    antigen_path = "./dags/files/iedb/antigen_uniprot.csv"

    columns_to_drop = ['uniProtkbId', 'lastSequenceUpdateDate', 'organismScientificName', 'proteinName',
        'cdAntigenNames', 'genes', 'functions', 'interactionText', 'pdb', 'alphafolddb', 'string', 'biogrid',
        'intact', 'naturalVariants']

    antigen = pd.read_csv(antigen_path)
    antigen = antigen.drop(columns=columns_to_drop)

    antigen.columns = ['name', 'sequence']

    antigen.to_csv("./dags/files/iedb/antigen_table.csv", index=False, index_label=False)


if __name__ == '__main__':
    drop_uniprot_columns()
