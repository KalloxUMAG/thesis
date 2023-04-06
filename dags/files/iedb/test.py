import pandas as pd

epitopes = pd.read_csv("./epitope.csv")

epitopes = epitopes.dropna(subset=['protein'])
epitopes = epitopes.drop_duplicates(subset=['name'])
count = 0

for index, row in epitopes.iterrows():
    protein = str(row['protein'])
    protein = protein.split(".")[1]
    if protein == "uniprot":
        count = count + 1

print(count)