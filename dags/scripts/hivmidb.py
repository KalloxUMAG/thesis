import pandas as pd
from scripts.helpers.requests import request_with_retry
from scripts.helpers.save_file import save_file
from scripts.helpers.remove_exist import remove_existing_epitopes

def download():
    files = pd.read_csv('./dags/files/hivmidb/urls.csv')

    for index, file in files.iterrows():
        name = file['filename']
        extension = file['extension']
        url = file['link']
        response = request_with_retry(url, 5)
        if not (response):
            print(f'Could not download the file {name}.{extension} from {url}.')
        else:
            save_file(name, response.content, extension, "./dags/files/hivmidb/downloads/")

def extract_epitopes():
    file_path = "./dags/files/hivmidb/downloads/epitopes.csv"

    epitopes = pd.read_csv(file_path)

    epitopes = epitopes.drop(index=epitopes.index[0], axis=0)
    epitopes = epitopes.drop(columns=['MAb Name', 'HXB2 start', 'HXB2 end', 
        'HXB2 start 2', 'HXB2 end 2', 'HXB2 DNA Contig', 
        'Subtype', 'Species'])
    epitopes.columns = ['sequence', 'protein', 'subprotein']
    epitopes.insert(0, 'name', epitopes['protein']+" "+epitopes['subprotein'])
    epitopes['database'] = "HIV MIDB"
    epitopes.to_csv('./dags/files/hivmidb/epitopes.csv', index=False, index_label=False)

def remove_epitopes():
    df = pd.read_csv('./dags/files/hivmidb/epitopes.csv')
    df2 = remove_existing_epitopes(df)
    df2.to_csv("./dags/files/hivmidb/epitopes.csv", index=False, index_label=False)

if __name__ == '__main__':
    download()
    extract_epitopes()