import pandas as pd

def join_antibodies():
    file_names = ['antibody', 'abcd', 'imgtgene', 'antibodypedia', 'cptc']

    df = pd.DataFrame()

    for file_name in file_names[:-1]:
        dataframe = pd.read_csv("./dags/files/uniprot/"+file_name+".csv")
        df = pd.concat([df,dataframe]).drop_duplicates()
    
    df.to_csv("./dags/files/uniprot/antibodies.csv", index=False, index_label=False)


if __name__ == '__main__':
    join_antibodies()
