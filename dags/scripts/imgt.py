import pandas as pd
import requests
import subprocess
from Bio.Seq import Seq

from helpers.requests import request_with_retry
from helpers.fasta_to_csv import extract_fasta_file

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
            print("La version ya se encuentra descargada")
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
    print("Elimnado")
    subprocess.Popen('uncompress ./dags/files/imgt/downloads/imgt.fasta.Z', shell=True).wait()
    print("Extraido")

    df = pd.DataFrame(columns=['name', 'sequence'])
    
    df = extract_fasta_file('./dags/files/imgt/downloads/imgt.fasta', df, '|', 0)

    print('Nucleotids to Protein sequence')

    df = nucleotic_to_protein(df)

    df.to_csv('./dags/files/imgt/antibodies.csv', index=False, index_label=False)

def nucleotic_to_protein(df):
    print("Convirtiendo nucleotidos a proteina")
    for index, antibody in df.iterrows():
        sequence = antibody['sequence']
        nucleotic_seq = Seq(sequence)
        if len(sequence)%3 == 1:
            nucleotic_seq = nucleotic_seq + Seq('N')
            print('Agregando N')
        if len(sequence)%3 == 1:
            nucleotic_seq = nucleotic_seq + Seq('N')
            print('Agregando N')
        protein_seq = nucleotic_seq.translate(stop_symbol='')
        protein_seq = str(protein_seq)
        df.loc[index] = [antibody['name'], protein_seq]
    
    return df