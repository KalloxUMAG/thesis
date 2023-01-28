import pandas as pd


def extract():
    dataset = pd.read_csv('./dags/files/covabdab/downloads/CoV-AbDab.csv')

    drop_columns = ['ABB Homology Model (if no structure)', 'Date Added', 'Update Description', 'Notes/Following Up?',
       'Ab or Nb', 'Binds to', "Doesn't Bind to", 'Neutralising Vs', 'Not Neutralising Vs', 'Protein + Epitope', 'Origin',
       'VHorVHH', 'VL', 'Heavy V Gene', 'Heavy J Gene', 'Light V Gene', 'Light J Gene', 'Structures', 'Sources', 'Last Updated']

    dataset = dataset.drop(columns=drop_columns)

    dataset.columns = ['name', 'cdrh3', 'cdrl3']
    dataset.to_csv('./dags/files/covabdab/covabdab-antibodies.csv', index=False, index_label=False)


if __name__ == '__main__':
    extract()
