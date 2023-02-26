import pandas as pd
import numpy as np
import subprocess
import os


def create_fasta(df, protein_folder):
    #Crea el archivo fasta dentro de una carpeta con el id de la proteina
    if os.path.exists(protein_folder+"/file.fasta"):
        print("Remove")
        os.remove(protein_folder+"/file.fasta")
    fasta = open(f"{protein_folder}/file.fasta", "w")
    for index,protein in df.iterrows():
        fasta.write(">"+protein['name']+"\n"+protein['sequence']+"\n")
    fasta.close()

def gene_ontology(temp_folder):
    file_path = temp_folder+"/file.fasta"
    output_path = temp_folder+"/result"
    print("GO en progreso...")
    command = [
        "metastudent",
        "-i",
        file_path,
        "-o",
        output_path,
        "--ontologies=MFO,BPO,CCO"
    ]

    try:
        subprocess.check_output(command)
        return 0
    except subprocess.CalledProcessError as e:
        return -1

def join_files(protein_folder,type):
    file_folder = protein_folder+"/"+type+".csv"
    if not os.path.exists(protein_folder+"/"+type+".csv"):
        output_file = open(protein_folder+"/"+type+".csv", "w")
        output_file.write("antigen,accession,probability,term")
        output_file.close()
    df = pd.read_csv(file_folder)
    df2 = pd.read_csv(protein_folder+"/result."+type+".txt", sep="\t", header=None)
    df2.rename(columns={0:"antigen",1:"accession",2:"probability",3:"term"}, inplace=True)
    df = pd.concat([df,df2]).drop_duplicates()
    df.to_csv(file_folder, index=False, index_label=False)
    os.remove(protein_folder+"/result."+type+".txt")


def prepare_gene_ontology(**kwargs):
    csv_path = kwargs['csv_path']
    database = kwargs['database']
    temp_folder = f"./dags/files/{database}/go"
    print(temp_folder)
    df = pd.read_csv(csv_path)
    
    rows = len(df.index)
    max_rows = 10

    #cantidad de splits
    max_files = int(rows/max_rows)
    if rows%max_rows!=0:
        max_files=max_files+1

    print(max_files)
    df_split = np.array_split(df,max_files)

    isExist = os.path.exists(temp_folder)
    if not isExist:
        os.makedirs(temp_folder)

    for i in range(0,max_files):
        print(len(df_split[i].index))
        create_fasta(df_split[i], temp_folder)
        print("Archivo fasta creado")
        status = gene_ontology(temp_folder)
        if(status == -1):
            print("Error")
            continue
        print("Uniendo archivos")
        join_files(temp_folder, "MFO")
        join_files(temp_folder, "BPO")
        join_files(temp_folder, "CCO")
    


if __name__ == '__main__':
    prepare_gene_ontology()
    