import subprocess

def pfam_domain():
    temp_file_path = "./dags/files/characterization/temp/fastas/temp1.fasta"
    output_path = "./dags/files/characterization/structural_characterization/"
    command = [
        "Predict_Property.sh",
        "-i",
        temp_file_path,
        "-o",
        output_path,
    ]
    subprocess.check_output(command)


if __name__ == '__main__':
    pfam_domain()
