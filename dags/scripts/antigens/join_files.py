import pandas as pd

def join_files():
    catnap = "./dags/files/catnap/antigen.csv"
    iedb = "./dags/files/iedb/antigen_table.csv"
    uniprot = "./dags/files/uniprot/antigen_table.csv"

    files = {'Catnap': catnap, 'IEDB': iedb, 'UniProt': uniprot}

    antigens = pd.DataFrame(columns=['name', 'sequence', 'database'])

    for database in files:
        df = pd.read_csv(files[database])
        df['database'] = database
        antigens = pd.concat([antigens, df], axis=0)
    
    antigens = antigens.drop_duplicates(subset=['name'])
    antigens = antigens.dropna(subset=['name'])

    antigens.to_csv("./dags/files/antigens/antigen.csv", index=False, index_label=False)


if __name__ == '__main__':
    join_files()
