from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from scripts.uniprot import download, extract_jsons, join_antibodies, drop_columns_antibody, antigen_tsv_to_csv

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

    end = EmptyOperator(task_id='end')

    start >> download_files >> extract_files >> join_antibodies_files >> [drop_antibody_columns, drop_antigen_columns] >> end
