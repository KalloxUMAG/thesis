import subprocess
import pandas as pd
import sys, os
import shutil

import warnings
warnings.filterwarnings("ignore")

def create_fasta(name, sequence, protein_folder):
    #Crea el archivo fasta dentro de una carpeta con el id de la proteina
    if os.path.exists(protein_folder):
        shutil.rmtree(protein_folder)
    os.makedirs(protein_folder)
    fasta = open(f"{protein_folder}/file.fasta", "w")
    fasta.write(">"+name+"\n"+sequence)
    fasta.close()

def structural_characterization(protein_folder):
    #Ejecuta Predict_Property
    temp_file_path = f"{protein_folder}/file.fasta"
    output_folder = protein_folder+"/"
    command = [
        "/home/kallox/respaldo/thesis/dags/scripts/characterization/Predict_Property/Predict_Property.sh",
        "-i",
        temp_file_path,
        "-o",
        output_folder,
    ]
    try:
        subprocess.check_output(command)
        return 0
    except subprocess.CalledProcessError as e:
        return -1

def get_results(protein_folder):
    #Lee los archivos con los resultados
    ss3_file = open(f"{protein_folder}/file.ss3_simp", 'r')
    ss8_file = open(f"{protein_folder}/file.ss3_simp", 'r')

    ss3 = ss3_file.readlines()[2]
    ss8 = ss8_file.readlines()[2]

    ss3_file.close()
    ss8_file.close()

    return [ss3[:-1], ss8[:-1]]

def structural_characterization_protein(protein_csv, protein_index, temp_folder):

    df = pd.read_csv(protein_csv)

    protein_df = df.iloc[[protein_index]]
    protein = protein_df.squeeze()
    protein_folder = f"{temp_folder}/{protein_index}"
    create_fasta(protein['name'], protein['sequence'], protein_folder)
    #En caso de error se termina la ejecucion
    if structural_characterization(protein_folder) == -1:
        shutil.rmtree(protein_folder)
        return
    results = get_results(protein_folder)
    protein['ss3'] = results[0]
    protein['ss8'] = results[1]
    shutil.rmtree(protein_folder)
    #El contenido del print es guardado como salida
    print(f"{protein['name']},{protein['sequence']},{protein['database']},{protein['ss8']},{protein['ss3']}")


if __name__ == '__main__':
    #Obtencion de argumentos
    protein_csv = sys.argv[1]
    protein_index = sys.argv[2]
    temp_folder = sys.argv[3]

    isExist = os.path.exists(temp_folder)
    if not isExist:
        os.makedirs(temp_folder)
    
    structural_characterization_protein(protein_csv, protein_index, temp_folder)
