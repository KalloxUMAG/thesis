import pandas as pd

df = pd.read_csv("./datasets/antibodies.csv")

for index, row in df.iterrows():
    #if row['sequence'].isnull():
    print(row['sequence'])
    input("")
    
