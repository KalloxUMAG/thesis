import pandas as pd


def drop_first_line(file_path):
    with open(file_path, 'r+') as fp:
        lines = fp.readlines()
        fp.seek(0)
        fp.truncate()

        fp.writelines(lines[1:])


def drop_columns_epitopes():
    file_path = "./dags/files/iedb/downloads/epitope_full_v3.csv"
    drop_first_line(file_path)
    epitope = pd.read_csv(file_path)
    columns_to_drop = [
       'Epitope Modified Residue(s)', 'Epitope Modification(s)',
    'Non-peptidic epitope IRI',
    'Parent Protein',
       'Parent Protein IRI', 'Organism Name', 'Organism IRI',
       'Parent Organism', 'Parent Organism IRI', 'Epitope Comments',
    'Non-peptidic object IRI',
       'Parent Protein.1',
       'Parent Protein IRI.1', 'Organism Name.1', 'Organism IRI.1',
       'Parent Organism.1', 'Parent Organism IRI.1', 'Epitope Synonyms', 'Epitope Relationship',
       'Synonyms','Antigen IRI.1', 'Antigen Name.1', 'Ending Position.1',
       'Starting Position.1', 'Description.1', 'Object Type.1', 
       'Starting Position', 'Ending Position', 'Antigen Name']

    epitope = epitope.drop(columns=columns_to_drop)

    epitope.columns = ['name', 'type', 'sequence', 'protein']

    epitope = epitope.reindex(columns=['name', 'sequence', 'protein', 'type'])

    epitope.to_csv('./dags/files/iedb/epitope.csv', index=False, index_label=False)


def drop_columns_antigens():
    file_path = "./dags/files/iedb/downloads/antigen_full_v3.csv"
    drop_first_line(file_path)
    antigen = pd.read_csv(file_path)
    columns_to_drop = [
      "Antigen Name", "Organism Name", "Organism ID", "# Epitopes", "# Assays", "# References"
    ]
    antigen = antigen.drop(columns=columns_to_drop)
    antigen.columns = ['link']
    antigen.to_csv("./dags/files/iedb/antigen.csv", index=False, index_label=False)


if __name__ == '__main__':
    drop_columns_antigens()
