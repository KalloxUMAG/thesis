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
    link = "https://rest.uniprot.org/uniprotkb/stream?fields=accession%2Cid%2Cprotein_name%2Csequence&format=tsv&query=%28antigen%29"
    filename = "antigens"
    extension = "tsv"

    for index, file in files.iterrows():
        get_protein(link, filename, extension)


if __name__ == '__main__':
    download()
