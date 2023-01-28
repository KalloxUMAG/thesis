import pandas as pd
import json
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

def extract_file(filename):

    columns_to_drop = ['Entry', 'Entry Name', 'Protein names']

    antigen = pd.read_csv(filename, sep='\t')
    antigen['name'] = antigen['proteinName'] + "||" + antigen['uniProtkbId'] + " || " + antigen['primaryAccession']
    antigen = antigen.drop(columns=columns_to_drop)

    antigen = antigen.reindex(columns=['name', 'sequence'])

    antigen.to_csv("./antigen_table.csv", index=False, index_label=False)
    

def extract():
    filename = "./antigens.csv"
    extract_file(filename)

if __name__ == "__main__":
    extract()