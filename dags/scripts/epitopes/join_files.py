import pandas as pd

def join_files():
    epitopes_files_path = {"hivmidb":"./dags/files/hivmidb/epitopes.csv", "eidb":"./dags/files/iedb/epitope.csv", "vdjdb":"./dags/files/vdjdb/epitopes.csv"}
    keys = [i for i in epitopes_files_path]
    epitopes = pd.DataFrame()

    for key in keys:
        df = pd.read_csv(epitopes_files_path[key])
        df['db'] = key
        epitopes = pd.concat([epitopes, df], axis=0)

    epitopes.to_csv("./dags/files/epitopes/epitopes.csv", index=False, index_label=False)


if __name__ == '__main__':
    join_files()
