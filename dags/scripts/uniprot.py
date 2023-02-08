import pandas as pd
import json
import warnings

from helpers.requests import request_with_retry
from helpers.save_file import save_file

warnings.simplefilter(action='ignore', category=FutureWarning)

def download():
    files = pd.read_csv('./dags/files/uniprot/urls.csv')

    for index, file in files.iterrows():
        name = file['filename']
        extension = file['extension']
        url = file['link']
        response = request_with_retry(url, 5)
        if not (response):
                print(f'Could not download the file {name}.{extension} from {url}.')
        save_file(name, response.content, extension, "./dags/files/uniprot/downloads/")

def extract_file(filename):

    with open('./dags/files/uniprot/downloads/'+filename+'.json', 'r') as f:
        data = json.load(f)

    cols = ['uniProtkbId', 'primaryAccession', 'lastSequenceUpdateDate', 'organismScientificName', 'proteinName', 'cdAntigenNames', 'genes', 'functions', 'interactionText', 'sequence', 'pdb', 'alphafolddb', 'string', 'biogrid', 'intact', 'naturalVariants']
    commentTypes = ['FUNCTION', 'SUBUNIT']

    df = pd.DataFrame(columns=cols)

    data = data['results']

    i = 1

    for protein in data:

        i = i + 1

        uniProtkbId = ''
        primaryAccession = ''
        lastSequenceUpdateDate = ''
        organismScientificName = ''
        proteinName = ''
        cdAntigenNames = []
        genes = []
        functions = ''
        interactionText = ''
        sequence = ''
        pdb = []
        alphafolddb = []
        string = ''
        biogrid = ''
        intact = ''
        naturalVariants = []

        if 'proteinDescription' in protein and 'recommendedName' in protein['proteinDescription']:
            if 'ecNumbers' in protein['proteinDescription']['recommendedName']:
                continue
            elif 'fullName' in protein['proteinDescription']['recommendedName']:
                proteinName = protein['proteinDescription']['recommendedName']['fullName']['value']

        uniProtkbId = protein['uniProtkbId']
        primaryAccession = protein['primaryAccession']
        lastSequenceUpdateDate = protein['entryAudit']['lastSequenceUpdateDate']
        if 'organism' in protein and 'scientificName' in protein['organism']:
            organismScientificName = protein['organism']['scientificName']


        if 'cdAntigenNames' in protein['proteinDescription']:
            for cdAntigenName in protein['proteinDescription']['cdAntigenNames']:
                cdAntigenNames.append(cdAntigenName['value'])

        if 'genes' in protein:
            for gen in protein['genes']:
                if 'geneName' in gen and 'value' in gen['geneName']:
                    genes.append(gen['geneName']['value'])

        if 'comments' in protein:
            for comment in protein['comments']:
                if comment['commentType'] == commentTypes[0]:
                    functions = comment['texts'][0]['value']

                if comment['commentType'] == commentTypes[1]:
                    interactionText = comment['texts'][0]['value']
        if 'sequence' in protein:
            sequence = protein['sequence']['value']

        if 'uniProtKBCrossReferences' in protein:
            for database in protein['uniProtKBCrossReferences']:
                if database['database'] == 'PDB':
                    pdb.append(database['id'])
                if database['database'] == 'AlphaFoldDB':
                    alphafolddb.append(database['id'])
                if database['database'] == 'STRING':
                    string = database['id']
                if database['database'] == 'BioGRID':
                    biogrid = database['id']
                if database['database'].lower() == 'intact':
                    intact = database['id']

        if 'features' in protein:
            for feature in protein['features']:
                if feature['type'] == 'Natural variant':
                    naturalVariants.append({'location': feature['location'], 'alternativeSequence': feature['alternativeSequence']})


        df = df.append({
                'uniProtkbId': uniProtkbId,
                'primaryAccession': primaryAccession,
                'organismScientificName': organismScientificName,
                'proteinName': proteinName,
                'cdAntigenNames': cdAntigenNames,
                'genes': genes,
                'functions': functions,
                'interactionText': interactionText,
                'sequence': sequence,
                'alphafolddb': alphafolddb,
                'pdb': pdb,
                'string': string,
                'biogrid': biogrid,
                'intact': intact,
                'naturalVariants': naturalVariants
            }, ignore_index=True)

        if i%1000 == 0 or i == 1:
            print(i)

    df.to_csv('./dags/files/uniprot/downloads/'+filename+'.csv', index=False, index_label=False)

def extract_jsons():
    files_dataframe = pd.read_csv('./dags/files/uniprot/urls.csv')
    for index, filename in files_dataframe.iterrows():
        if filename['extension'] == "json":
            extract_file(filename['filename'])

def join_antibodies():
    file_names = ['antibody', 'abcd', 'imgtgene', 'antibodypedia', 'cptc']

    df = pd.DataFrame()

    for file_name in file_names[:-1]:
        dataframe = pd.read_csv("./dags/files/uniprot/downloads/"+file_name+".csv")
        df = pd.concat([df,dataframe]).drop_duplicates()
    
    df.to_csv("./dags/files/uniprot/antibodies.csv", index=False, index_label=False)

def drop_columns_antigen():
    antigen_path = "./dags/files/uniprot/antigen.csv"

    columns_to_drop = ['uniProtkbId', 'primaryAccession', 'lastSequenceUpdateDate', 'organismScientificName', 'proteinName',
        'cdAntigenNames', 'genes', 'functions', 'interactionText', 'pdb', 'alphafolddb', 'string', 'biogrid',
        'intact', 'naturalVariants']

    antigen = pd.read_csv(antigen_path)
    antigen['name'] = antigen['proteinName'] + " || " + antigen['uniProtkbId'] + " || " + antigen['primaryAccession']
    antigen = antigen.drop(columns=columns_to_drop)

    antigen.to_csv("./dags/files/uniprot/antigen_table.csv", index=False, index_label=False)


def drop_columns_antibody():
    antibodies_path = "./dags/files/uniprot/antibodies.csv"

    columns_to_drop = ['uniProtkbId', 'primaryAccession', 'lastSequenceUpdateDate', 'organismScientificName', 'proteinName',
        'cdAntigenNames', 'genes', 'functions', 'interactionText', 'pdb', 'alphafolddb', 'string', 'biogrid',
        'intact', 'naturalVariants']
    
    antibodies = pd.read_csv(antibodies_path)
    antibodies['name'] = antibodies['proteinName'] + "||" + antibodies['uniProtkbId'] + " || " + antibodies['primaryAccession']
    antibodies = antibodies.drop(columns=columns_to_drop)

    antibodies = antibodies.reindex(columns=['name', 'sequence'])
    antibodies.to_csv("./dags/files/uniprot/antibodies_table.csv", index=False, index_label=False)