import pandas as pd

def join_files():
    catnap = "./dags/files/catnap/seqs_aa.csv"
    covabdab = "./dags/files/covabdab/covabdab-antibodies.csv"
    imgt = "./dags/files/imgt/antibodies.csv"
    uniprot = "./dags/files/uniprot/antibodies_table.csv"
    vdjdb = "./dags/files/vdjdb/antibodies.csv"

    files = {'Catnap':catnap, 'CoV-Abdab':covabdab, 'IMGT':imgt, 'UniProt':uniprot, 'VDJdb':vdjdb}

    antibodies = pd.DataFrame(columns=['name', 'sequence', 'database'])

    for database in files:
        df = pd.read_csv(files[database])
        df['database'] = database
        antibodies = pd.concat([antibodies, df], axis=0)
    
    antibodies = antibodies.drop_duplicates(subset=['name'])
    antibodies = antibodies.fillna('-')
    antibodies.to_csv("./dags/files/antibodies/antibodies.csv", index=False, index_label=False)


if __name__ == '__main__':
    join_files()