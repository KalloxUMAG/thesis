import requests
import zipfile
import pandas as pd


def get_file(url, name, extension):
    response = requests.get(url)
    if response.status_code == 200:
        print(f'{name} downloaded.')
        save_file(name, response.content, extension)
        unzip_file(name)
    else:
        print(f'Could not download the file {name}.{extension} from {url}.')


def save_file(name, content, extension):
    file = open('./dags/files/iedb/downloads/'+name+'.'+extension, 'wb')
    file.write(content)
    file.close()
    print(f'{name}.{extension} saved.')


def unzip_file(name):
    with zipfile.ZipFile('./dags/files/iedb/downloads/'+name+'.zip', 'r') as zip_ref:
        zip_ref.extractall('./dags/files/iedb/downloads')


def download():
    files = pd.read_csv('./dags/scripts/iedb/urls.csv')

    for index, file in files.iterrows():
        get_file(file['link'], file['filename'], file['extension'])


if __name__ == '__main__':
    download()
