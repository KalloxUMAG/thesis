#Catnap tiene un periodo de actualizacion de 1 mes. Debe ser descargado solo el 1 de cada mes.abs(
import requests
import pandas as pd


def get_file(url, name, extension):
    response = requests.get(url)
    if response.status_code == 200:
        print(f'{name} downloaded.')
        save_file(name, response.content, extension)
    else:
        print(f'Could not download the file {name}.{extension} from {url}.')


def save_file(name, content, extension):
    file = open('./dags/files/catnap/downloads/'+name+'.'+extension, 'wb')
    file.write(content)
    file.close()
    print(f'{name}.{extension} saved.')


def download():
    files = pd.read_csv('./dags/scripts/catnap/urls.csv')
    for index, file in files.iterrows():
        get_file(file['link'], file['filename'], file['extension'])


if __name__ == '__main__':
    download()
