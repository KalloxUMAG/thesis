import sys, os
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


def extract_fasta(fasta_file, dataframe, separator, split_position):
    # Read in FASTA
    cols = dataframe.columns
    file = open(fasta_file, 'r')
    lines = file.readlines()
    i = 1
    id = ''
    sequence = ''
    for line in lines:
        if line[0] == '>':
            if i > 1:
                dataframe = dataframe.append({
                    cols[0] : id,
                    cols[1] : sequence
                }, ignore_index = True)
            id = ''
            sequence = ''
            linecontent = line[1:]
            linecontent = linecontent.split(separator)
            id = linecontent[split_position]
            i = i + 1
        elif len(line) > 0:
            linecontent = line[:-1]
            sequence = sequence + linecontent
            i = i + 1
    dataframe = dataframe.append({
                    cols[0] : id,
                    cols[1] : sequence
                }, ignore_index = True)
    file.close()
    return dataframe


def extract():
    #Antibodies files
    light_chain = './dags/files/catnap/downloads/Antibody_light_chain_aa_sequences.fasta'
    heavy_chain = './dags/files/catnap/downloads/Antibody_heavy_chain_aa_sequences.fasta'

    light_dataframe = pd.DataFrame(columns=['name', 'light_sequence'])
    heavy_dataframe = pd.DataFrame(columns=['name', 'heavy_sequence'])

    light_dataframe = extract_fasta(light_chain, light_dataframe, '_', 0)
    heavy_dataframe = extract_fasta(heavy_chain, heavy_dataframe, '_', 0)

    df = pd.merge(light_dataframe, heavy_dataframe, on='name', how='left')
    #Elimina los duplicados... Se debe buscar una forma de extraer el nombre correcta del fasta
    df = df.drop_duplicates(subset=['name'])
    df.to_csv('./dags/files/catnap/seqs_aa.csv', index=False, index_label=False)

    #Viruses file
    viruses = './dags/files/catnap/downloads/Virus_aa_alignment.tsv'

    virus_dataframe = pd.DataFrame(columns=['name', 'sequence'])

    virus_dataframe = extract_fasta(viruses, virus_dataframe, '.', 3)

    virus_dataframe.to_csv('./dags/files/catnap/antigen.csv', index=False, index_label=False)



if __name__ == '__main__':
    extract()
