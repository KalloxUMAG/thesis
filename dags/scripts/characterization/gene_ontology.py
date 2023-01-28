"""Gene ontology module"""
import subprocess
import os


def gene_ontology():
    fasta_path = "./files/characterization/antibodies.fasta"
    #fasta_path = "./files/characterization/test.fasta"
    temp_fasta_path = "./files/characterization/temp/"

    fasta = open(fasta_path, "r")
    num_lines = sum(1 for line in fasta)
    start_line = 0
    file_number = 0
    num_sequences = 10
    fasta.seek(0)
    while num_lines > 0:
        file_number = file_number + 1
        temp_fasta = open(f'{temp_fasta_path}fastas/temp{file_number}.fasta', 'w')
        for line in fasta.readlines()[start_line:(start_line + num_sequences)]:
            temp_fasta.write(line)
        fasta.seek(0)
        start_line = start_line + num_sequences
        num_lines = num_lines - num_sequences
        temp_fasta.close()
    fasta.close()

    fasta_files = os.listdir(temp_fasta_path+"fastas/")
    quantity = 0
    for fasta_file in fasta_files:
        quantity = quantity + 1
        temp_fasta_file = temp_fasta_path+"fastas/"+fasta_file
        output_path = temp_fasta_path+"outputs/"+fasta_file

        command = [
                "metastudent",
                "-i",
                temp_fasta_file,
                "-o",
                output_path,
            ]

        subprocess.check_output(command)
        print(quantity)
    

if __name__ == '__main__':
    gene_ontology()
    