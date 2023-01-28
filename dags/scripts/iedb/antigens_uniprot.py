import pandas as pd
import requests
from time import time
#from requests.exceptions import ConnectTimeout
from requests.exceptions import Timeout, HTTPError, ConnectionError

def request_with_retry(request, MAX_RETRIES):
    for i in range(MAX_RETRIES):
        try:
            r = requests.get(request, timeout=100)
            r.raise_for_status()
            return r
        except ConnectionError as ce:
            print("Antigen does not exist")
            return False
        except Timeout as tout:
            print(f'TimeOut Error, retrying ({i}/{MAX_RETRIES})')
        except HTTPError as err:
            print(r.status_code)
            if r.status_code == 429:
                print(r.content)
                time.sleep(int(r.headers["Retry-After"])+5)
            else:
                return False
    return False


def get_proteins(uniprot_ids):
    api_preffix = "https://rest.uniprot.org/uniprotkb/"
    api_suffix = ".json"

    cols = ['uniProtkbId', 'primaryAccession', 'lastSequenceUpdateDate', 'organismScientificName', 'proteinName', 'cdAntigenNames', 'genes', 'functions', 'interactionText', 'sequence', 'pdb', 'alphafolddb', 'string', 'biogrid', 'intact', 'naturalVariants']

    antigens = pd.DataFrame(columns=cols)
    count = 0
    total = len(uniprot_ids)
    for id in uniprot_ids:
        count = count + 1
        api_link = f'{api_preffix}{id}{api_suffix}'

        response = request_with_retry(api_link, 5)
        if not(response):
            continue
        else:
            print(f'{id} downloaded.')
            antigen = extract_data(dict(response.json()))
            if len(antigen) != 0:
                antigens = antigens.append(antigen, ignore_index=True)
            else:
                print("The antigen was a enzime")
        print(f'{count}/{total}')
        
    antigens.to_csv("./dags/files/iedb/antigen_uniprot.csv", index=False, index_label=False)


def extract_data(protein):
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

    commentTypes = ['FUNCTION', 'SUBUNIT']
    if protein['entryType'] == "Inactive":
        return {}
    if 'proteinDescription' in protein and 'recommendedName' in protein['proteinDescription']:
        if 'ecNumbers' in protein['proteinDescription']['recommendedName']:
            return {}
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


    return {
        'uniProtkbId': uniProtkbId,
        'primaryAccession': primaryAccession,
        'lastSequenceUpdateDate': lastSequenceUpdateDate,
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
    }


def antigens_uniprot():
    
    antigen_file = "./dags/files/iedb/antigen.csv"
    uniprot_ids = []

    antigen = pd.read_csv(antigen_file)

    for index, line in antigen.iterrows():
        if "uniprot" in line['link']:
            id = line['link'].split('/')[4]
            uniprot_ids.append(id)
    
    get_proteins(uniprot_ids)




if __name__ == '__main__':
    antigens_uniprot()
