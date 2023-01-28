import pandas as pd


def swap_columns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df


def extract_antibodies():
    file_path = "./dags/files/vdjdb/downloads/epitopes.tsv"
    epitopes = pd.read_csv(file_path, sep='\t')

    epitopes = epitopes.drop(columns=['complex.id', 'Gene', 'V', 'J', 'Species', 'MHC A',
        'MHC B', 'MHC class', 'Reference', 'Method', 'Epitope',
        'Meta', 'CDR3fix', 'Score', 'Epitope gene', 'Epitope species'])

    #epitopes = swap_columns(epitopes, 'CDR3', 'Epitope')
    #epitopes.columns = ['sequence', 'protein']
    epitopes.insert(0, 'name', epitopes['CDR3'])
    epitopes.columns = ['name', 'cdr3']
    epitopes.to_csv("./dags/files/vdjdb/antibodies.csv", index=False, index_label=False)


if __name__ == '__main__':
    extract_antibodies()

#CDR3