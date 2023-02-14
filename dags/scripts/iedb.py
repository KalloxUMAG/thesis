import pandas as pd
import zipfile

from helpers.requests import request_with_retry
from helpers.save_file import save_file
from helpers.drop_first_line import drop_first_line
from helpers.extract_json_uniprot import extract_json_uniprot

def unzip_file(name):
    with zipfile.ZipFile('./dags/files/iedb/downloads/'+name+'.zip', 'r') as zip_ref:
        zip_ref.extractall('./dags/files/iedb/downloads')

def download():
    files = pd.read_csv('./dags/files/iedb/urls.csv')

    for index, file in files.iterrows():
        name = file['filename']
        extension = file['extension']
        url = file['link']
        response = request_with_retry(url, 5)
        if not (response):
            print(f'Could not download the file {name}.{extension} from {url}.')
        else:
            save_file(name, response.content, extension, "./dags/files/iedb/downloads/")
            unzip_file(name)

def drop_columns_epitopes():
    file_path = "./dags/files/iedb/downloads/epitope_full_v3.csv"
    drop_first_line(file_path)
    epitope = pd.read_csv(file_path)
    columns_to_drop = [
       'Epitope Modified Residue(s)', 'Epitope Modification(s)',
    'Non-peptidic epitope IRI',
    'Parent Protein',
       'Parent Protein IRI', 'Organism Name', 'Organism IRI',
       'Parent Organism', 'Parent Organism IRI', 'Epitope Comments',
    'Non-peptidic object IRI',
       'Parent Protein.1',
       'Parent Protein IRI.1', 'Organism Name.1', 'Organism IRI.1',
       'Parent Organism.1', 'Parent Organism IRI.1', 'Epitope Synonyms', 'Epitope Relationship',
       'Synonyms','Antigen IRI.1', 'Antigen Name.1', 'Ending Position.1',
       'Starting Position.1', 'Description.1', 'Object Type.1', 
       'Starting Position', 'Ending Position', 'Antigen Name']

    epitope = epitope.drop(columns=columns_to_drop)

    epitope.columns = ['name', 'type', 'sequence', 'protein']

    epitope = epitope.reindex(columns=['name', 'sequence', 'protein', 'type'])

    epitope.to_csv('./dags/files/iedb/epitope.csv', index=False, index_label=False)

def download_antigens():
    api_preffix = "https://rest.uniprot.org/uniprotkb/"
    api_suffix = ".json"

    file_path = "./dags/files/iedb/downloads/antigen_full_v3.csv"
    drop_first_line(file_path)
    antigen = pd.read_csv(file_path)
    antigens_url = antigen['Antigen ID'].to_list()
    antigens_url = [x for x in antigens_url if x != None]

    antigens = pd.DataFrame(columns=['name', 'sequence', 'database'])
    
    for antigen_url in antigens_url:
        if "uniprot" in antigen_url:
            id = antigen_url.split('/')[-1]
            url = f'{api_preffix}{id}{api_suffix}'
            response = request_with_retry(url, 5)
            if not (response):
                print(f'Could not download the antigen {id} from {url}.')
            else:
                antigen = extract_json_uniprot(response.json())
                if len(antigen) == 0:
                    continue
                antigen["database"] = "UniProt"
                antigens = antigens.append(antigen, ignore_index=True)
    antigens.to_csv("./dags/files/iedb/antigens.csv", index=False, index_label=False)


if __name__ == '__main__':
    drop_columns_epitopes()