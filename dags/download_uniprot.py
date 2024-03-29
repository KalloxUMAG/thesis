from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from scripts.uniprot import download, extract_jsons, join_antibodies, drop_columns_antibody, antigen_tsv_to_csv, remove_antibodies, remove_antigens, load_antibodies_to_db, load_antigens_to_db
from scripts.characterization.gene_ontology import prepare_gene_ontology

default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2022, 11, 3, 21, 0, 0)
}

with DAG(dag_id='download_uniprot', default_args=default_args, schedule='@monthly') as dag:
    start = EmptyOperator(task_id='start')

    download_files = PythonOperator(task_id='download_files', python_callable=download)

    extract_files = PythonOperator(task_id='extract_files', python_callable=extract_jsons)

    join_antibodies_files = PythonOperator(task_id='join_antibodies_files', python_callable=join_antibodies)

    drop_antibody_columns = PythonOperator(task_id='drop_antibody_columns', python_callable=drop_columns_antibody)
    
    drop_antigen_columns = PythonOperator(task_id='drop_gen_columns', python_callable=antigen_tsv_to_csv)

    remove_existing_antibodies = PythonOperator(task_id='remove_existing_antibodies', python_callable=remove_antibodies)

    remove_existing_antigens = PythonOperator(task_id='remove_existing_antigens', python_callable=remove_antigens)

    structural_prediction_antibodies = BashOperator(task_id='structural_prediction_antibodies', bash_command="/home/kallox/respaldo/thesis/dags/scripts/characterization/execute.sh uniprot/antibodies_table.csv uniprot ")

    structural_prediction_antigens = BashOperator(task_id='structural_prediction_antigens', bash_command="/home/kallox/respaldo/thesis/dags/scripts/characterization/execute.sh uniprot/antigen_table.csv uniprot ")

    #gene_ontology = PythonOperator(task_id='gene_ontology', python_callable=prepare_gene_ontology, op_kwargs={'csv_path': './dags/files/uniprot/antigen_table.csv', 'database': 'uniprot'})

    load_antibodies = PythonOperator(task_id='load_antibodies', python_callable=load_antibodies_to_db)

    load_antigens = PythonOperator(task_id='load_antigens', python_callable=load_antigens_to_db)

    end = EmptyOperator(task_id='end')

    start >> download_files >> extract_files >> join_antibodies_files >> [drop_antibody_columns, drop_antigen_columns] >> remove_existing_antibodies >> remove_existing_antigens >> structural_prediction_antibodies >> structural_prediction_antigens >> load_antibodies >> load_antigens >> end
