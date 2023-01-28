import requests
import pandas as pd
import os


def get_protein(url, name, extension):
    response = requests.get(url)
    if response.status_code == 200:
        print(f'{name} downloaded.')
        save_file(name, response.content, extension)
    else:
        print(f'Could not download the file {name}.{extension} from {url}.')


def save_file(name, content, extension):
    file = open('./dags/files/uniprot/downloads/'+name+'.'+extension, 'wb')
    file.write(content)
    file.close()
    print(f'{name}.{extension} saved.')


def download():
    print(os.getcwd())
    files = pd.read_csv('./dags/scripts/uniprot/urls.csv')

    for index, file in files.iterrows():
        get_protein(file['link'], file['filename'], file['extension'])


if __name__ == '__main__':
    download()
