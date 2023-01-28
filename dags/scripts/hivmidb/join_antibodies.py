import pandas as pd
import os

def join_antibodies():
    files = fasta_files = os.listdir("./dags/files/hivmidb/downloads/")
    antibodies = pd.DataFrame()
    for file in files:
        if file == "epitopes.csv":
            continue
        filedf = pd.read_csv(f'./dags/files/hivmidb/downloads/{file}')
        filedf = filedf.drop(columns=filedf.columns[22:])
        antibodies = pd.concat([antibodies, filedf], axis=0)
    
    
    antibodies = antibodies.drop_duplicates()
    antibodies.to_csv("./dags/files/hivmidb/antibodies.csv")


if __name__ == '__main__':
    join_antibodies()