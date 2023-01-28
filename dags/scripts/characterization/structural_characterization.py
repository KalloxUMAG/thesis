import subprocess
import pandas as pd
import multiprocessing
import sys, os

def create_fasta(name, sequence, index, folder):
    os.makedirs(temp_folder+"/"+index)
    fasta = open(f"{folder}/{index}/file.fasta", "w")
    fasta.write(">"+name+"\n"+sequence)
    fasta.close()

def structural_characterization(index):
    temp_file_path = f"./dags/files/characterization/structural_characterization/{folder}/file.fasta"
    output_path = f"./dags/files/characterization/structural_characterization/{folder}"
    command = [
        "Predict_Property.sh",
        "-i",
        temp_file_path,
        "-o",
        output_path,
    ]
    try:
        subprocess.check_output(command)
        return 0
    except subprocess.CalledProcessError as e:
        print(e.output)
        return -1

def read_results(folder):
    ss3_file = open(f"./dags/files/characterization/structural_characterization/{folder}/file.ss3_simp", 'r')
    ss8_file = open(f"./dags/files/characterization/structural_characterization/{folder}/file.ss3_simp", 'r')

    ss3 = ss3_file.readlines()[2]
    ss8 = ss8_file.readlines()[2]

    ss3_file.close()
    ss8_file.close()

    return [ss3[:-1], ss8[:-1]]

def multiprocesado(df, index):
    antibody = df.iloc[index]
    print(antibody)
    if antibody['sequence'] != '-':
        print(antibody['name'])
        result = structural_characterization(antibody['name'], antibody['sequence'], "antibodies")
        if result == 0:
            results = read_results("antibodies")
            antibody['ss3'] = results[0]
            antibody['ss8'] = results[1]
    return antibody

def structural_characterization_antibody(antibody_csv, antibody_index, temp_folder):
    
    df = pd.read_csv(antibody_csv)

    antibody = df.iloc[[antibody_index]]
    create_fasta(antibody['name'], antibody['sequence'], antibody_index, temp_folder)
    #structural_characterization
    
    #print(antibody)


if __name__ == '__main__':
    antibody_csv = sys.argv[1]
    antibody_index = sys.argv[2]
    temp_folder = sys.argv[3]

    isExist = os.path.exists(temp_folder)
    if not isExist:
        os.makedirs(temp_folder)
        print("New folder created")
    
    structural_characterization_antibody(antibody_csv, antibody_index, temp_folder)
