import pandas as pd
import requests


def get_file(url, name, extension):
    response = requests.get(url)
    if response.status_code == 200:
        print(f'{name} downloaded.')
        save_file(name, response.content, extension)
    else:
        print(f'Could not download the file {name}.{extension} from {url}.')


def save_file(name, content, extension):
    file = open('./dags/files/hivmidb/downloads/'+name+'.'+extension, 'wb')
    file.write(content)
    file.close()
    print(f'{name}.{extension} saved.')


def download():
    files = pd.read_csv('./dags/scripts/hivmidb/urls.csv')

    for index, file in files.iterrows():
        get_file(file['link'], file['filename'], file['extension'])


if __name__ == '__main__':
    download()