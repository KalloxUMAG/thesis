import pandas as pd

def extract_epitopes():
    file_path = "./dags/files/hivmidb/downloads/epitopes.csv"

    epitopes = pd.read_csv(file_path)

    epitopes = epitopes.drop(index=epitopes.index[0], axis=0)
    epitopes = epitopes.drop(columns=['MAb Name', 'HXB2 start', 'HXB2 end', 
        'HXB2 start 2', 'HXB2 end 2', 'HXB2 DNA Contig', 
        'Subtype', 'Species'])
    epitopes.columns = ['sequence', 'protein', 'subprotein']
    epitopes.insert(0, 'name', epitopes['protein']+" "+epitopes['subprotein'])

    epitopes.to_csv('./dags/files/hivmidb/epitopes.csv', index=False, index_label=False)


if __name__ == '__main__':
    extract_epitopes()
