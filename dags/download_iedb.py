from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from scripts.iedb import download, drop_columns_epitopes, download_antigens, remove_epitopes, remove_antigens

default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2022, 11, 3, 21, 20, 0)
}

with DAG(dag_id='download_iedb', default_args=default_args, schedule='@monthly') as dag:
    start = EmptyOperator(task_id='start')

    download_files = PythonOperator(task_id='download_files', python_callable=download)

    drop_epitopes = PythonOperator(task_id='drop_epitopes', python_callable=drop_columns_epitopes)

    download_antigens_uniprot = PythonOperator(task_id='download_antigens_uniprot', python_callable=download_antigens)

    remove_existing_epitopes = PythonOperator(task_id='remove_existing_epitopes', python_callable=remove_epitopes)

    remove_existing_antigens = PythonOperator(task_id='remove_existing_antigens', python_callable=remove_antigens)

    end = EmptyOperator(task_id='end')

    start >> download_files >> drop_epitopes >> download_antigens_uniprot >> remove_existing_antigens >> remove_existing_epitopes >> end
