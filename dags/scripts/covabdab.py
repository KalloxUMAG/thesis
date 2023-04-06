from lxml import html
import pandas as pd

from scripts.helpers.requests import request_with_retry
from scripts.helpers.save_file import save_file
from scripts.helpers.remove_exist import remove_existing_antibodies
from scripts.helpers.load import load_antibodies_db

def download():
    
    url = 'http://opig.stats.ox.ac.uk/webapps/covabdab/'

    response = request_with_retry(url, 5)
    if not (response):
                print(f'Could not download from {url}.')
    page = response
    tree = html.fromstring(page.content)
    date = str(tree.xpath('/html/body/div[2]/div/div[2]/div/p/text()[7]'))
    date = date[date.find(':')+2:date.find(')')]
    print(date)

    file_url = str(tree.xpath('//*[@id="collapseOne"]/div/a[1]/@href'))
    file_url = file_url[2:-2].split('/')[5]

    download_url = url + 'static/downloads/' + file_url
    print(download_url)
    response = request_with_retry(download_url, 5)
    if not (response):
        print(f'Could not download the file from {url}.')
    else:
        save_file('CoV-AbDab', response.content, 'csv', "./dags/files/covabdab/downloads/")

def extract():
    dataset = pd.read_csv('./dags/files/covabdab/downloads/CoV-AbDab.csv')

    drop_columns = ['ABB Homology Model (if no structure)', 'Date Added', 'Update Description', 'Notes/Following Up?',
       'Ab or Nb', 'Binds to', "Doesn't Bind to", 'Neutralising Vs', 'Not Neutralising Vs', 'Protein + Epitope', 'Origin',
       'VHorVHH', 'VL', 'Heavy V Gene', 'Heavy J Gene', 'Light V Gene', 'Light J Gene', 'Structures', 'Sources', 'Last Updated']

    dataset = dataset.drop(columns=drop_columns)

    dataset.columns = ['name', 'cdrh3', 'cdrl3']
    dataset['database'] = "CoV-Abdab"
    dataset.to_csv('./dags/files/covabdab/covabdab-antibodies.csv', index=False, index_label=False)

def remove_antibodies():
    df = pd.read_csv('./dags/files/covabdab/covabdab-antibodies.csv')
    df2 = remove_existing_antibodies(df)
    df2.to_csv("./dags/files/covabdab/antibodies.csv", index=False, index_label=False)

def load_antibodies_to_db():
    df = pd.read_csv("./dags/files/covabdab/antibodies.csv")
    load_antibodies_db(df)

if __name__ == '__main__':
    download()
    extract()