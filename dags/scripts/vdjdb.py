from lxml import html, etree
import pandas as pd
import zipfile
import os

from scripts.helpers.requests import request_with_retry
from scripts.helpers.save_file import save_file

def unzip_file(name):
    with zipfile.ZipFile('./dags/files/vdjdb/downloads/'+name+'.zip', 'r') as zip_ref:
        zip_ref.extractall('./dags/files/vdjdb/downloads')


def download():
    url = "https://github.com/antigenomics/vdjdb-db/releases/latest"

    response = request_with_retry(url, 5)
    if not (response):
        print(f'Could not download from {url}.')
    version = response.url.split("tag/")[1]

    download_url = f"https://github.com/antigenomics/vdjdb-db/releases/download/{version}/vdjdb-{version}.zip"

    response = request_with_retry(download_url, 5)
    if not (response):
        print(f'Could not download from {download_url}.')
        return
    save_file("vdjdb", response.content, "zip", "./dags/files/vdjdb/downloads/")
    unzip_file("vdjdb")
    for file_name in os.listdir("./dags/files/vdjdb/downloads/"):
        file = "./dags/files/vdjdb/downloads/"+file_name
        if file_name != "vdjdb.txt" and file_name != ".gitkeep":
            os.remove(file)
    os.rename("./dags/files/vdjdb/downloads/vdjdb.txt", "./dags/files/vdjdb/downloads/vdjdb.tsv")

def swap_columns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df


def extract_antibodies():
    file_path = "./dags/files/vdjdb/downloads/vdjdb.tsv"
    epitopes = pd.read_csv(file_path, sep='\t')

    epitopes = epitopes.drop(columns=['complex.id', 'Gene', 'V', 'J', 'Species', 'MHC A',
        'MHC B', 'MHC class', 'Reference', 'Method', 'Epitope',
        'Meta', 'CDR3fix', 'Score', 'Epitope gene', 'Epitope species'])

    epitopes.insert(0, 'name', epitopes['CDR3'])
    epitopes.columns = ['name', 'cdr3']
    epitopes.to_csv("./dags/files/vdjdb/antibodies.csv", index=False, index_label=False)


def extract_epitopes():
    file_path = "./dags/files/vdjdb/downloads/vdjdb.tsv"
    epitopes = pd.read_csv(file_path, sep='\t')

    epitopes = epitopes.drop(columns=['complex.id', 'Gene', 'V', 'J', 'CDR3', 'Species', 'MHC A',
        'MHC B', 'MHC class', 'Reference', 'Method',
        'Meta', 'CDR3fix', 'Score'])

    epitopes.insert(2, 'protein', epitopes['Epitope species'] + ' ' + epitopes['Epitope gene'])
    epitopes.insert(0, 'name', epitopes['Epitope'])
    epitopes = epitopes.drop(columns=['Epitope gene', 'Epitope species'])
    epitopes.columns = ['name', 'sequence', 'protein']
    epitopes.to_csv("./dags/files/vdjdb/epitopes.csv", index=False, index_label=False)

if __name__ == '__main__':
    download()