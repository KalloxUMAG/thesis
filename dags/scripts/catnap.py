#Catnap tiene un periodo de actualizacion de 1 mes. Debe ser descargado solo el 1 de cada mes.abs(
import pandas as pd

from helpers.requests import request_with_retry
from helpers.save_file import save_file
from helpers.fasta_to_csv import extract_fasta_file


def download():
    files = pd.read_csv('./dags/files/catnap/urls.csv')

    for index, file in files.iterrows():
        name = file['filename']
        extension = file['extension']
        url = file['link']
        response = request_with_retry(url, 5)
        if not (response):
            print(f'Could not download the file {name}.{extension} from {url}.')
        else:
            save_file(name, response.content, extension, "./dags/files/catnap/downloads/")

def extract():
    light_chain = './dags/files/catnap/downloads/Antibody_light_chain_aa_sequences.fasta'
    heavy_chain = './dags/files/catnap/downloads/Antibody_heavy_chain_aa_sequences.fasta'

    light_dataframe = pd.DataFrame(columns=['name', 'light_sequence'])
    heavy_dataframe = pd.DataFrame(columns=['name', 'heavy_sequence'])

    light_dataframe = extract_fasta_file(light_chain, light_dataframe, '_', 0)
    heavy_dataframe = extract_fasta_file(heavy_chain, heavy_dataframe, '_', 0)

    df = pd.merge(light_dataframe, heavy_dataframe, on='name', how='left')

    df = df.drop_duplicates(subset=['name'])
    df.to_csv('./dags/files/catnap/seqs_aa.csv', index=False, index_label=False)

    viruses = './dags/files/catnap/downloads/Virus_aa_alignment.fasta'

    virus_dataframe = pd.DataFrame(columns=['name', 'sequence'])

    virus_dataframe = extract_fasta_file(viruses, virus_dataframe, '.', 3)

    virus_dataframe.to_csv('./dags/files/catnap/antigen.csv', index=False, index_label=False)

if __name__ == '__main__':
    download()
    extract()