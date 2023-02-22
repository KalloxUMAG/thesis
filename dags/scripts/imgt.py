import pandas as pd
import requests
import subprocess
from Bio.Seq import Seq

from scripts.helpers.requests import request_with_retry
from scripts.helpers.fasta_to_csv import extract_fasta_file
from scripts.helpers.remove_exist import remove_existing_antibodies

def check_release():
    url = "https://www.imgt.org/download/LIGM-DB/currentRelease"
    response = request_with_retry(url, 5)

    old_release = 0
    
    if not (response):
        print("Error getting current release")
        return False
    else:
        current_release = response.content.decode()
        f = open('./dags/files/imgt/current_release.txt', 'r')
        old_release = f.readline()
        f.close()

        if old_release == current_release:
            print("Version already downloaded")
            return False
        else:
            f = open('./dags/files/imgt/current_release.txt', 'w')
            f.write(current_release)
            f.close()
            return True

def download():
    if not(check_release()):
        return
    
    url = "https://www.imgt.org/download/LIGM-DB/imgt.fasta.Z"
    response = request_with_retry(url, 5)
    if not (response):
        print("Error getting file")
        return
    
    f = open('./dags/files/imgt/downloads/imgt.fasta.Z', 'wb')
    f.write(response.content)
    f.close()

    subprocess.Popen('rm ./dags/files/imgt/downloads/imgt.fasta', shell=True).wait()
    print("Old fasta deleted")
    subprocess.Popen('uncompress ./dags/files/imgt/downloads/imgt.fasta.Z', shell=True).wait()
    print("New fasta extracted")

    df = pd.DataFrame(columns=['name', 'sequence'])

    print("Converting fasta to csv")
    
    df = extract_fasta_file('./dags/files/imgt/downloads/imgt.fasta', df, '|', 0)

    print('Nucleotids to Protein sequence')

    df = nucleotic_to_protein(df)
    df['database'] = "IMGT"
    df.to_csv('./dags/files/imgt/antibodies.csv', index=False, index_label=False)

def nucleotic_to_protein(df):
    print("Converting nucleotids to protein")
    for index, antibody in df.iterrows():
        sequence = antibody['sequence']
        nucleotic_seq = Seq(sequence)
        if len(sequence)%3 == 1:
            nucleotic_seq = nucleotic_seq + Seq('N')
            print('N added')
        if len(sequence)%3 == 1:
            nucleotic_seq = nucleotic_seq + Seq('N')
            print('N added')
        protein_seq = nucleotic_seq.translate(stop_symbol='')
        protein_seq = str(protein_seq)
        df.loc[index] = [antibody['name'], protein_seq]
    
    return df

def remove_antibodies():
    df = pd.read_csv('./dags/files/imgt/antibodies.csv')
    df2 = remove_existing_antibodies(df)
    df2.to_csv("./dags/files/imgt/antibodies.csv", index=False, index_label=False)

if __name__ == '__main__':
    download()