import pandas as pd


def csv_to_fasta():
    csv_path = './files/uniprot/antibodies.csv'
    antibodies = pd.read_csv(csv_path)
    antibodies = antibodies.drop(columns=['primaryAccession', 'lastSequenceUpdateDate', 'organismScientificName', 'proteinName', 'cdAntigenNames', 'genes', 'functions', 'interactionText', 'pdb', 'alphafolddb', 'intact', 'biogrid', 'naturalVariants', 'string'])

    fasta = open("./files/characterization/antibodies.fasta", "w")

    for index, antibody in antibodies.iterrows():
        
        uniProtkbId = ">uniProtkbId:"+antibody['uniProtkbId']
        sequence = antibody['sequence']

        fasta.write(uniProtkbId+"\n"+sequence+"\n")
        print(index)
    fasta.close()


if __name__ == '__main__':
    csv_to_fasta()
