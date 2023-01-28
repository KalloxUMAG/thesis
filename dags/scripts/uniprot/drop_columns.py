import pandas as pd

def drop_columns_antigen():
    antigen_path = "./dags/files/uniprot/antigen.csv"

    columns_to_drop = ['uniProtkbId', 'primaryAccession', 'lastSequenceUpdateDate', 'organismScientificName', 'proteinName',
        'cdAntigenNames', 'genes', 'functions', 'interactionText', 'pdb', 'alphafolddb', 'string', 'biogrid',
        'intact', 'naturalVariants']

    antigen = pd.read_csv(antigen_path)
    antigen['name'] = antigen['uniProtkbId'] + " || " + antigen['primaryAccession']
    antigen = antigen.drop(columns=columns_to_drop)

    #antigen.columns = ['name', 'sequence']

    antigen.to_csv("./dags/files/uniprot/antigen_table.csv", index=False, index_label=False)


def drop_columns_antibody():
    antibodies_path = "./dags/files/uniprot/antibodies.csv"

    columns_to_drop = ['uniProtkbId', 'primaryAccession', 'lastSequenceUpdateDate', 'organismScientificName', 'proteinName',
        'cdAntigenNames', 'genes', 'functions', 'interactionText', 'pdb', 'alphafolddb', 'string', 'biogrid',
        'intact', 'naturalVariants']
    
    antibodies = pd.read_csv(antibodies_path)
    antibodies['name'] = antibodies['proteinName'] + "||" + antibodies['uniProtkbId'] + " || " + antibodies['primaryAccession']
    antibodies = antibodies.drop(columns=columns_to_drop)

    #antibodies.columns = ['name', 'sequence']
    antibodies = antibodies.reindex(columns=['name', 'sequence'])
    antibodies.to_csv("./dags/files/uniprot/antibodies_table.csv", index=False, index_label=False)


if __name__ == '__main__':
    drop_columns_antibody()
    drop_columns_antigen()
